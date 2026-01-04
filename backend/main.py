from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
from pydantic import BaseModel
import uvicorn
import os

# Import Routers
from backend.routes import chat, todos

app = FastAPI(title="Todo API with Dapr (HTTP)")

# --- CORS MIDDLEWARE ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- INCLUDE ROUTERS ---
# Frontend expects /api/chat and /api/tasks
app.include_router(chat.router, prefix="/api")
app.include_router(todos.router, prefix="/api")

# --- DAPR CONFIGURATION ---
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", 3500)
PUBSUB_NAME = "kafka-pubsub"
TOPIC_NAME = "todo-events"

class CloudEvent(BaseModel):
    data: Dict[str, Any]
    type: str
    source: str
    id: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Event-Driven Todo API!"}

# --- DAPR SUBSCRIBER ---
@app.get("/dapr/subscribe")
def subscribe():
    return [{
        "pubsubname": PUBSUB_NAME,
        "topic": TOPIC_NAME,
        "route": "events/todo-created"
    }]

@app.post("/events/todo-created")
def event_handler(event: CloudEvent):
    print(f"📣 RECEIVED EVENT from Kafka: {event.data}")
    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
