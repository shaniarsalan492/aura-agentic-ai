import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

KB_DIR = os.path.dirname(__file__)
PERSIST_DIR = os.path.join(KB_DIR, "chroma_store")

def query_knowledge_base(query, k=2):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    vectorstore = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )

    results = vectorstore.similarity_search(query, k=k)

    print(f"\nQuery: {query}\n")
    for i, doc in enumerate(results, 1):
        print(f"--- Result {i} ---")
        print(doc.page_content)
        print(f"(source: {doc.metadata.get('source')})\n")

if __name__ == "__main__":
    query_knowledge_base("What is the refund policy if my order is delayed?")