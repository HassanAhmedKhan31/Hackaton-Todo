# Task ID: T-024 (Recurring Service)
from fastapi import FastAPI, Request
from pydantic import BaseModel
from dapr.clients import DaprClient
import uvicorn
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("recurring-service")

app = FastAPI(title="Recurring Task Service")

class TaskEventData(BaseModel):
    event_type: str | None = None
    id: int
    title: str
    user_id: str | None = None
    is_recurring: bool | None = False
    recurrence_interval: str | None = None

class CloudEvent(BaseModel):
    data: TaskEventData
    type: str
    source: str
    id: str
    specversion: str
    datacontenttype: str | None = None

@app.get("/")
def read_root():
    return {"status": "Recurring Service Operational"}

@app.post("/task-events")
async def handle_task_event(event: CloudEvent):
    """
    Consumer for task-events topic.
    """
    data = event.data
    logger.info(f"Received event: {data}")

    # Logic: Only handle 'completed' events for recurring tasks
    if data.event_type == "completed" and data.is_recurring:
        logger.info(f"Processing recurring task: {data.title}")
        
        # Create new task via Dapr Service Invocation
        new_title = f"{data.title} (Recurring)"
        new_task_payload = {
            "title": new_title,
            "description": f"Auto-generated from task {data.id}",
            "user_id": data.user_id,
            "is_recurring": True, # The new task is also recurring
            "recurrence_interval": data.recurrence_interval
        }

        try:
            with DaprClient() as d:
                # invoke_method(app_id, method_name, data, content_type, http_verb)
                resp = d.invoke_method(
                    app_id="backend",
                    method_name="tasks/", # The backend route is /tasks/
                    data=json.dumps(new_task_payload),
                    content_type="application/json",
                    http_verb="POST"
                )
                logger.info(f"Successfully created recurring task via Dapr: {resp.status_code}")
        except Exception as e:
            logger.error(f"Failed to create recurring task: {e}")

    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
