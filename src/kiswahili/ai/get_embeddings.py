from langchain_ollama import OllamaEmbeddings

def get_embedding_function():
    embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url="https://29aa-34-105-88-194.ngrok-free.app/")
    return embeddings