from pathlib import Path
from typing import List

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from config import (
    OPENAI_API_KEY,
    CHROMA_PERSIST_DIR,
    EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    VECTOR_STORE,
)

LOADER_MAP = {
    ".pdf": PyPDFLoader,
    ".docx": Docx2txtLoader,
    ".txt": TextLoader,
    ".md": UnstructuredMarkdownLoader,
}


def load_document(file_path: str) -> List[Document]:
    ext = Path(file_path).suffix.lower()
    loader_cls = LOADER_MAP.get(ext)
    if not loader_cls:
        raise ValueError(f"Unsupported file type: {ext}")
    return loader_cls(file_path).load()


def split_documents(docs: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        add_start_index=True,
    )
    return splitter.split_documents(docs)


def get_embeddings():
    return OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY)


def get_vector_store(embeddings=None):
    if embeddings is None:
        embeddings = get_embeddings()

    if VECTOR_STORE == "pinecone":
        from langchain_pinecone import PineconeVectorStore
        from config import PINECONE_INDEX
        return PineconeVectorStore(index_name=PINECONE_INDEX, embedding=embeddings)

    return Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings,
    )


def ingest_file(file_path: str) -> int:
    docs = load_document(file_path)
    chunks = split_documents(docs)
    embeddings = get_embeddings()
    store = get_vector_store(embeddings)
    store.add_documents(chunks)
    return len(chunks)
