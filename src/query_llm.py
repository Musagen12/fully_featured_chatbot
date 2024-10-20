from src.governance_chatbot.ai.ai_router import query_chroma_db

def process_input(user_query: str):
    llm_response = query_chroma_db(query_text=user_query)
    return llm_response
