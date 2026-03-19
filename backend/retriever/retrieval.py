import os
from ingestion.embedder import embed_query
from retriever.vector_store import query_collection

TOP_K = int(os.getenv("TOP_K", 5))


def retrieve(query: str, session_id: str) -> list[dict]:
    """
    Full retrieval pipeline for a user query:
    1. Embed the query
    2. Search the session's vector store
    3. Return top-k relevant chunks with metadata

    Returns list of dicts:
    [{ "text": "...", "source": "file.pdf", "chunk_index": 3, "score": 0.87 }]
    """
    query_vector = embed_query(query)
    results = query_collection(query_vector, session_id, top_k=TOP_K)
    return results