from sentence_transformers import SentenceTransformer
import numpy as np

# all-MiniLM-L6-v2 — fast, lightweight, strong for semantic similarity
# Downloads once on first run, cached locally after that
_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """
    Takes list of chunk dicts from chunker.py.
    Adds an "embedding" key (numpy array → list of floats) to each chunk.
    Returns the same list enriched with embeddings.
    """
    texts = [chunk["text"] for chunk in chunks]

    # encode returns a numpy array of shape (n_chunks, 384)
    embeddings = _model.encode(texts, show_progress_bar=False, normalize_embeddings=True)

    for i, vector in enumerate(embeddings):
        chunks[i]["embedding"] = vector.tolist()

    return chunks


def embed_query(query: str) -> list[float]:
    """
    Embeds a single user query string.
    normalize_embeddings=True ensures cosine similarity = dot product.
    Returns a flat list of floats (384 dimensions).
    """
    vector = _model.encode([query], normalize_embeddings=True)
    return vector[0].tolist()