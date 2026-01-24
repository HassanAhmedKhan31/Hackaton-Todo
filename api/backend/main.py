from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Dict, Any
from pydantic import BaseModel
import uvicorn
import os

# Import Routers
# These imports are now relative to the current package (api.backend)
from .routes import chat, todos
from .database import init_db
from .fix_schema import migrate

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Apply schema migrations on startup
    migrate()
    # Initialize DB on startup
    init_db()
    yield

# Initialize FastAPI app
# redirect_slashes=True (default) helps handle cases where a client 
# might include or omit a trailing slash.
app = FastAPI(title="Todo API", redirect_slashes=True, lifespan=lifespan)

# --- CORS MIDDLEWARE ---
# In a production environment, you should be more restrictive.
# For Vercel deployments, `allow_origin_regex` handles preview and production URLs.
# You can also explicitly add your production URL if you have a custom domain or specific needs.
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    os.getenv("VERCEL_URL"), # Dynamically add Vercel production URL if available
    "httpshttps://hackathon-todo-git-feat-k8s-final-himo-al.vercel.app", # Placeholder for your production URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- INCLUDE ROUTERS ---
# We include the routers without an additional prefix here.
# Ensure that inside 'todos.py', the prefix is set to "/tasks" 
# and inside 'chat.py', it is set to "/chat".
app.include_router(chat.router)
app.include_router(todos.router)

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

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Backend is reachable"}

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

# Create a root app and mount the existing app under /api
# The docs for the sub-app will now be available at /api/docs
root_app = FastAPI()
root_app.mount("/api", app)

if __name__ == "__main__":
    # Standard development port
    # It is recommended to use the string 'backend.main:app' for 
    # better compatibility with reloader and lazy-loading of routes.
    uvicorn.run("api.backend.main:root_app", host="0.0.0.0", port=8000, reload=True)