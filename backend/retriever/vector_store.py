import numpy as np
import faiss

# In-memory store — session_id → { "index": faiss.Index, "chunks": list[dict] }
# No persistence. Fresh on every server start.
_sessions: dict[str, dict] = {}

VECTOR_DIM = 384  # all-MiniLM-L6-v2 output dimension


def store_chunks(chunks: list[dict], session_id: str) -> None:
    """
    Builds a FAISS IndexFlatIP (inner product) index for the session.
    Because embeddings are L2-normalized, inner product == cosine similarity.
    Stores the raw chunks alongside for text retrieval.
    """
    vectors = np.array([chunk["embedding"] for chunk in chunks], dtype=np.float32)

    # IndexFlatIP = exact search using inner product (cosine when normalized)
    index = faiss.IndexFlatIP(VECTOR_DIM)
    index.add(vectors)

    # Store index + chunk metadata (without embeddings to save memory)
    clean_chunks = []
    for chunk in chunks:
        clean_chunks.append({
            "text": chunk["text"],
            "metadata": chunk["metadata"]
        })

    _sessions[session_id] = {
        "index": index,
        "chunks": clean_chunks
    }


def query_collection(query_embedding: list[float], session_id: str, top_k: int = 5) -> list[dict]:
    """
    Runs cosine similarity search (via FAISS inner product) for the session.
    Returns top_k results as list of dicts with text + metadata + score.
    """
    if session_id not in _sessions:
        return []

    session = _sessions[session_id]
    index: faiss.IndexFlatIP = session["index"]
    chunks: list[dict] = session["chunks"]

    query_vec = np.array([query_embedding], dtype=np.float32)

    # scores = cosine similarity (0.0 to 1.0), ids = chunk positions
    k = min(top_k, index.ntotal)
    scores, ids = index.search(query_vec, k)

    results = []
    for score, idx in zip(scores[0], ids[0]):
        if idx == -1:
            continue
        chunk = chunks[idx]
        results.append({
            "text": chunk["text"],
            "source": chunk["metadata"].get("source", "unknown"),
            "chunk_index": chunk["metadata"].get("chunk_index", 0),
            "score": round(float(score), 4)
        })

    return results


def delete_collection(session_id: str) -> None:
    """
    Removes the session's FAISS index and chunks from memory.
    Call this when the user ends their session.
    """
    _sessions.pop(session_id, None)