import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHUNK_SIZE    = int(os.getenv("CHUNK_SIZE", 512))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 64))

_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=["\n\n", "\n", ".", " ", ""],  # tries largest break first
    length_function=len,
)


def chunk_text(text: str, filename: str) -> list[dict]:
    """
    Splits raw text using RecursiveCharacterTextSplitter.
    Tries to break at paragraphs → newlines → sentences → words.

    Returns list of dicts:
    [{ "text": "...", "metadata": { "source": "file.pdf", "chunk_index": 0 } }]
    """
    raw_chunks = _splitter.split_text(text)

    chunks = []
    for index, chunk in enumerate(raw_chunks):
        chunks.append({
            "text": chunk.strip(),
            "metadata": {
                "source": filename,
                "chunk_index": index
            }
        })

    return chunks