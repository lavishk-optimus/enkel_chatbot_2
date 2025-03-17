from fastapi import APIRouter, FastAPI
from backend.services.langgraph_integration import chatbot_response

router = APIRouter()
app = FastAPI()

@router.post("/chat-llm")
def chat_with_llm(user_query: str):
    """Handle user queries with integrated expense categorization and vendor detection"""
    answer = chatbot_response(user_query)
    return {"answer": answer}