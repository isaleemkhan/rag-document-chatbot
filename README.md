# RAG Document Chatbot

Upload PDFs, Word docs, or text files and ask questions — get cited, streaming answers powered by GPT-4o and a full RAG pipeline.

![Demo](docs/demo.gif)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Next.js Frontend                     │
│   FileUpload ──► POST /upload          ChatWindow ──► POST /chat  │
└──────────────────────┬──────────────────────────┬───────────┘
                       │                          │
┌──────────────────────▼──────────────────────────▼───────────┐
│                     FastAPI Backend                          │
│                                                             │
│  /upload                              /chat                 │
│  ┌──────────┐                        ┌─────────────────┐   │
│  │  ingest  │                        │  retriever      │   │
│  │  ├ load  │                        │  ├ MMR search   │   │
│  │  ├ chunk │                        │  └ reranker     │   │
│  │  └ embed │                        └────────┬────────┘   │
│  └──────┬───┘                                 │            │
│         │                          ┌──────────▼─────────┐  │
│  ┌──────▼──────────────────┐       │  LangChain chain   │  │
│  │  Vector Store           │       │  ├ prompt template │  │
│  │  ChromaDB (dev)         │       │  ├ GPT-4o stream   │  │
│  │  Pinecone  (prod)       │       │  └ source citation │  │
│  └─────────────────────────┘       └────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- OpenAI API key

### 1. Clone & configure

```bash
git clone https://github.com/isaleemkhan/rag-document-chatbot.git
cd rag-document-chatbot
cp .env.example .env
# Fill in your OPENAI_API_KEY in .env
```

### 2. Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r ../requirements.txt
uvicorn main:app --reload
# API running at http://localhost:8000
```

### 3. Frontend

```bash
cd frontend
npm install
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
# UI running at http://localhost:3000
```

### 4. Docker (full stack)

```bash
docker compose up --build
```

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | — | Required. Your OpenAI key |
| `VECTOR_STORE` | `chroma` | `chroma` for local, `pinecone` for prod |
| `CHROMA_PERSIST_DIR` | `./chroma_db` | ChromaDB storage path |
| `PINECONE_API_KEY` | — | Required if using Pinecone |
| `PINECONE_INDEX` | `rag-docs` | Pinecone index name |
| `LLM_MODEL` | `gpt-4o` | Any OpenAI chat model |
| `LLM_TEMPERATURE` | `0` | 0 = deterministic |

---

## API Reference

### `POST /upload`
Upload a document for ingestion.

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@report.pdf"
# {"filename": "report.pdf", "chunks_indexed": 42}
```

### `POST /chat`
Stream an answer grounded in uploaded documents.

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the key findings?", "rerank": false}'
```

---

## Supported File Types

| Format | Extension |
|---|---|
| PDF | `.pdf` |
| Word | `.docx` |
| Plain text | `.txt` |
| Markdown | `.md` |

---

## Deployment

### Vercel (frontend)
```bash
cd frontend
npx vercel --prod
# Set NEXT_PUBLIC_API_URL to your backend URL in Vercel env settings
```

### Railway / Render (backend)
- Point to `backend/` directory
- Set env vars from `.env.example`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Production vector store
Switch from ChromaDB to Pinecone by setting `VECTOR_STORE=pinecone` and providing your Pinecone credentials.

---

## Tech Stack

| Layer | Tech |
|---|---|
| LLM | GPT-4o (OpenAI) |
| Orchestration | LangChain |
| Embeddings | text-embedding-3-small |
| Vector DB (dev) | ChromaDB |
| Vector DB (prod) | Pinecone |
| Backend | FastAPI + uvicorn |
| Frontend | Next.js 14 (App Router) |
| Styling | Tailwind CSS |
| Containerization | Docker + Compose |
