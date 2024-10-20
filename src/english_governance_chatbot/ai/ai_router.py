from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from .get_embeddings import get_embedding_function
import os

base_url = os.getenv("OLLAMA_HOST")

CHROMA_PATH = "/home/kerich/Documents/azure-speech/src/governance_chatbot/chroma"
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def query_chroma_db(query_text: str):
    """Query the Chroma DB for a specific question"""
    
    # Prepare the DB and embedding function
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        
    # Search for the most relevant documents
    results = db.similarity_search_with_score(query_text, k=5)
    if not results:
        return {"response": "No relevant documents found", "sources": []}

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    # Prepare the prompt
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Get response from LLM
    model = OllamaLLM(model="mistral", base_url=base_url)
    response_text = model.invoke(prompt)

    return {"response": response_text}