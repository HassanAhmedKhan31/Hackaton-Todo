# Task ID: T-022 (Event Publishing)
# Task ID: T-024 (Recurring Logic)
import logging
import time
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlmodel import Session
from dapr.clients import DaprClient
from ..database import get_session, engine # Import engine for background tasks
from ..models import Task
from ..service import TodoService
from ..agent import agent

# Configure logger
logger = logging.getLogger("backend.routes.todos")
logging.basicConfig(level=logging.INFO)

# --- CRITICAL: This must be named 'router' ---
router = APIRouter(prefix="/tasks", tags=["tasks"])

# --- Background Functions ---

def publish_event(pubsub_name: str, topic_name: str, data: Dict[str, Any]):
    """(Background) Publish an event to a Dapr pub/sub topic."""
    try:
        with DaprClient() as d:
            d.publish_event(pubsub_name=pubsub_name, topic_name=topic_name, data=data)
        logger.info(f"BG: Successfully published event to topic '{topic_name}' for task ID {data.get('id')}")
    except Exception as e:
        logger.warning(f"BG: Failed to publish event to topic '{topic_name}' via Dapr: {e}")

def process_ai_agent_logic(task_id: int, title: str):
    """(Background) Calls the AI agent to process the task and updates the description."""
    logger.info(f"BG: Starting AI processing for task {task_id} ('{title}')...")
    
    # Create a new, independent session for the background task
    with Session(engine) as session:
        try:
            # 1. Call the actual AI agent with the task title
            user_message = f"Add a task: '{title}'"
            ai_generated_text = agent.run(user_message)

            # 2. Update the task in the database with the AI's response
            TodoService.update_task(session=session, task_id=task_id, description=ai_generated_text)
            
            logger.info(f"BG: Successfully completed AI processing and updated task {task_id}.")

        except Exception as e:
            logger.error(f"BG: AI processing failed for task {task_id}: {e}")


@router.get("/", response_model=List[Task])
def read_tasks(session: Session = Depends(get_session)):
    """Read all tasks."""
    logger.info("GET /tasks called")
    return TodoService.get_tasks(session)

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: Task, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    """
    Create a new task, returning a response immediately.
    Schedules background tasks for AI processing and event publishing.
    """
    logger.info(f"API: Creating task '{task.title}'")
    
    # 1. Save the initial task to the database (This is fast)
    created_task = TodoService.create_task(
        session, 
        title=task.title, 
        description=task.description or "AI is thinking...", # Set initial description
        user_id=task.user_id,
    )
    logger.info(f"API: Task {created_task.id} created in DB.")

    # 2. Schedule background tasks (These do not block the response)
    background_tasks.add_task(process_ai_agent_logic, created_task.id, created_task.title)
    
    event_data = {"event_type": "created", "id": created_task.id, "title": created_task.title}
    background_tasks.add_task(publish_event, "kafka-pubsub", "task-events", event_data)
    
    logger.info(f"API: AI processing and event publishing for task {created_task.id} scheduled.")

    # 3. Return the initial task object to the frontend immediately
    return created_task

@router.get("/{task_id}", response_model=Task)
def read_task(task_id: int, session: Session = Depends(get_session)):
    task = TodoService.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: Task, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    """Update a task and publish an event if completed."""
    updated_task = TodoService.update_task(
        session,
        task_id=task_id,
        title=task_update.title,
        description=task_update.description,
        status=task_update.status,
    )
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if updated_task.status == "completed":
        event_data = {"event_type": "completed", "id": updated_task.id, "title": updated_task.title}
        background_tasks.add_task(publish_event, "kafka-pubsub", "task-events", event_data)

    return updated_task

@router.delete("/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    success = TodoService.delete_task(session, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"ok": True}
