from generation.prompts import get_prompt


def build_prompt(
    query: str,
    chunks: list[dict],
    user_type: str = "Human"
) -> tuple[str, str]:
    """
    Assembles the full prompt for the LLM.

    Returns:
        system_prompt (str) — injected as the system message
        user_message  (str) — the user's question

    Chunks are formatted with source citations inline so the LLM
    can reference them naturally in its answer.
    """
    if not chunks:
        context = "No relevant content found in the uploaded document."
    else:
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            source = chunk.get("source", "unknown")
            idx = chunk.get("chunk_index", 0)
            text = chunk.get("text", "").strip()
            context_parts.append(
                f"[{i}] Source: {source} | Chunk #{idx}\n{text}"
            )
        context = "\n\n---\n\n".join(context_parts)

    system_prompt = get_prompt(user_type).format(context=context)
    user_message = query

    return system_prompt, user_message