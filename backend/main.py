import uuid
import os
from dotenv import load_dotenv
import uvicorn
import traceback


load_dotenv()

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


from ingestion.loader import load_document
from ingestion.chunker import chunk_text
from ingestion.embedder import embed_chunks
from retriever.vector_store import store_chunks, delete_collection
from retriever.retrieval import retrieve
from generation.builder import build_prompt
from generation.llm import call_llm

app = FastAPI(title="YourLegal API", version="1.0.0")

# Allow frontend (any origin during dev — tighten in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────
# Request / Response schemas
# ─────────────────────────────────────────

class ChatRequest(BaseModel):
    session_id: str
    message: str
    user_type: str = "human"

class ChatResponse(BaseModel):
    answer: str
    sources: list[dict]

class UploadResponse(BaseModel):
    session_id: str
    filename: str
    chunks_stored: int
    message: str

class SessionDeleteResponse(BaseModel):
    session_id: str
    message: str


# ─────────────────────────────────────────
# Routes
# ─────────────────────────────────────────

@app.get("/")
def health_check():
    return {"status": "YourLegal API is running"}


@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Accepts a PDF or DOCX file.
    Runs the full ingestion pipeline:
      load → chunk → embed → store in session vector store
    Returns a session_id the frontend must use for all /chat calls.
    """
    allowed = {"pdf", "docx"}
    ext = file.filename.lower().split(".")[-1]
    if ext not in allowed:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")

    file_bytes = await file.read()
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        # 1. Extract text
        raw_text = load_document(file_bytes, file.filename)

        # 2. Split into chunks
        chunks = chunk_text(raw_text, file.filename)

        # 3. Embed chunks
        embedded_chunks = embed_chunks(chunks)

        # 4. Store in a fresh in-memory session collection
        session_id = str(uuid.uuid4())
        store_chunks(embedded_chunks, session_id)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

    return UploadResponse(
        session_id=session_id,
        filename=file.filename,
        chunks_stored=len(embedded_chunks),
        message="Document uploaded and indexed. You can now chat."
    )


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Accepts a user message + session_id.
    Runs retrieval → prompt assembly → LLM call.
    Returns the answer with source citations.
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
        # 1. Retrieve relevant chunks
        chunks = retrieve(request.message, request.session_id)

        # 2. Build prompt
        system_prompt, user_message = build_prompt(
            query=request.message,
            chunks=chunks,
            user_type=request.user_type
        )

        # 3. Call LLM
        answer = call_llm(system_prompt, user_message)

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

    # Return answer + sources (without raw embeddings)
    sources = [
        {"source": c["source"], "chunk_index": c["chunk_index"], "score": c["score"]}
        for c in chunks
    ]

    return ChatResponse(answer=answer, sources=sources)


@app.delete("/delete/{session_id}", response_model=SessionDeleteResponse)
def end_session(session_id: str):
    """
    Clears the in-memory vector collection for this session.
    Call this when the user closes the chat.
    """
    delete_collection(session_id)
    return SessionDeleteResponse(
        session_id=session_id,
        message="Session cleared successfully."
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)