from typing import AsyncIterator
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from retriever import get_retriever
from config import OPENAI_API_KEY, LLM_MODEL, LLM_TEMPERATURE

SYSTEM_PROMPT = """You are a helpful assistant that answers questions strictly based on the provided context.
If the answer is not in the context, say you don't have enough information.
Always cite the source document and page number when available.

Context:
{context}"""

HUMAN_PROMPT = "{question}"


def format_docs(docs):
    parts = []
    for i, doc in enumerate(docs):
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page", "")
        ref = f"[{i+1}] {source}" + (f", page {page}" if page else "")
        parts.append(f"{ref}\n{doc.page_content}")
    return "\n\n---\n\n".join(parts)


def build_chain(rerank: bool = False):
    retriever = get_retriever(rerank=rerank)
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", HUMAN_PROMPT),
    ])
    llm = ChatOpenAI(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        openai_api_key=OPENAI_API_KEY,
        streaming=True,
    )
    return (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )


async def stream_answer(question: str, rerank: bool = False) -> AsyncIterator[str]:
    chain = build_chain(rerank=rerank)
    async for chunk in chain.astream(question):
        yield chunk
