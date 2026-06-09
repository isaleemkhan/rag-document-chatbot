import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "rag-docs")
PINECONE_ENV = os.getenv("PINECONE_ENV", "us-east-1")

VECTOR_STORE = os.getenv("VECTOR_STORE", "chroma")  # "chroma" | "pinecone"
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")

EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0"))

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 5
