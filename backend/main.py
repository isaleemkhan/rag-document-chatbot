import os
import shutil
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from ingest import ingest_file
from chain import stream_answer

app = FastAPI(title="RAG Document Chatbot", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPPORTED_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
    "text/markdown",
}


class ChatRequest(BaseModel):
    question: str
    rerank: bool = False


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if file.content_type not in SUPPORTED_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")

    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        n_chunks = ingest_file(tmp_path)
    finally:
        os.unlink(tmp_path)

    return {"filename": file.filename, "chunks_indexed": n_chunks}


@app.post("/chat")
async def chat(req: ChatRequest):
    async def event_stream():
        async for token in stream_answer(req.question, rerank=req.rerank):
            yield token

    return StreamingResponse(event_stream(), media_type="text/plain")
