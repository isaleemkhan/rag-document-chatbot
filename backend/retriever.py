from typing import List
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

from ingest import get_vector_store
from config import TOP_K


def get_base_retriever(store=None):
    if store is None:
        store = get_vector_store()
    return store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": TOP_K, "fetch_k": TOP_K * 3},
    )


def get_retriever(rerank: bool = False):
    retriever = get_base_retriever()
    if not rerank:
        return retriever

    encoder = HuggingFaceCrossEncoder(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")
    compressor = CrossEncoderReranker(model=encoder, top_n=TOP_K)
    return ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=retriever,
    )


def retrieve(query: str, rerank: bool = False) -> List[Document]:
    retriever = get_retriever(rerank=rerank)
    return retriever.invoke(query)
