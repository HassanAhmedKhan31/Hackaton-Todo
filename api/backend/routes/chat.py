from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from ..agent import agent 

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Run the agent (which now uses Mimo-v2-flash reasoning)
        response_text = agent.run(request.message)
        
        if not response_text:
            raise Exception("Model returned an empty response.")
            
        return ChatResponse(response=str(response_text))
    except Exception as e:
        # If you still see 401, check your .env file for the correct key
        raise HTTPException(status_code=500, detail=f"Agent Error: {str(e)}")