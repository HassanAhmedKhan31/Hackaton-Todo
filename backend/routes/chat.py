# Task ID: T-014
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from backend.agent import agent

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint for the AI Chatbot.
    Receives a user message, runs the Agent, and returns the response.
    """
    try:
        response_text = agent.run(request.message)
        return ChatResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
