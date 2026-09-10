from app.config.settings import USE_LOCAL_EMBEDDINGS, LOCAL_EMBEDDING_MODEL, EMBEDDING_MODEL


def get_embeddings():
    """Returns the active embedding provider based on the USE_LOCAL_EMBEDDINGS toggle
    in settings.py. Local embeddings are free and unlimited for development; Gemini
    embeddings are used for the final production build."""
    if USE_LOCAL_EMBEDDINGS:
        from langchain_huggingface import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(model_name=LOCAL_EMBEDDING_MODEL)
    else:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        return GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)