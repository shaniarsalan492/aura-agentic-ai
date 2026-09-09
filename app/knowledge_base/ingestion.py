import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from app.config.settings import EMBEDDING_MODEL, CHROMA_DIR, KNOWLEDGE_BASE_DIR


def build_vectorstore():
    docs = []
    for filename in os.listdir(KNOWLEDGE_BASE_DIR):
        if filename.endswith(".txt"):
            loader = TextLoader(os.path.join(KNOWLEDGE_BASE_DIR, filename), encoding="utf-8")
            docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

    print(f"Vector store built with {len(chunks)} chunks at {CHROMA_DIR}")


if __name__ == "__main__":
    build_vectorstore()