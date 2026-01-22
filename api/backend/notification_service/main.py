# Task ID: T-023 (Notification Consumer)
# Task ID: T-025 (Reminders)
from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
import logging
import requests
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("notification-service")

app = FastAPI(title="Notification Service")

# Dapr Configuration
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", 3500)
DAPR_URL = f"http://localhost:{DAPR_HTTP_PORT}/v1.0-alpha1/jobs"

class TaskEvent(BaseModel):
    id: int
    title: str
    user_id: str | None = None
    remind_at: str | None = None

class CloudEvent(BaseModel):
    data: TaskEvent
    type: str
    source: str
    id: str
    specversion: str
    datacontenttype: str | None = None

class JobPayload(BaseModel):
    task_id: int
    title: str
    user_id: str | None

@app.get("/")
def read_root():
    return {"status": "Notification Service Operational"}

@app.post("/task-events")
async def handle_task_event(event: CloudEvent):
    """
    Consumer for task-events topic.
    """
    logger.info("received event")
    task = event.data
    logger.info(f"Notification Sent: Task '{task.title}' (ID: {task.id}) created for User '{task.user_id}'")
    
    # Schedule Reminder if remind_at is set
    if task.remind_at:
        logger.info(f"Scheduling reminder for task {task.id} at {task.remind_at}")
        job_name = f"reminder-{task.id}"
        
        # We schedule the job on the local sidecar.
        # The job will callback THIS service when triggered.
        # Dapr Jobs callback defaults to POST /job/<job_name> usually, 
        # but we can probably specify data to route it or use a standardized name.
        # Actually, let's assume we use the name to route in a generic handler or specific handler.
        # But wait, Dapr Jobs API allows defining the payload.
        
        job_payload = {
            "name": job_name,
            "dueTime": task.remind_at,
            "data": {
                "@type": "type.googleapis.com/google.protobuf.StringValue",
                "value": str(JobPayload(task_id=task.id, title=task.title, user_id=task.user_id).model_dump_json())
            }
        }
        
        try:
            # We must use the Sidecar URL
            # Note: In K8s, localhost refers to the pod, so sidecar is accessible on localhost if injected.
            resp = requests.post(f"{DAPR_URL}/{job_name}", json=job_payload)
            if resp.status_code in [200, 204]:
                logger.info(f"Successfully scheduled job {job_name}")
            else:
                logger.error(f"Failed to schedule job: {resp.status_code} {resp.text}")
        except Exception as e:
            logger.error(f"Error scheduling job: {e}")

    return {"status": "success"}

# Callback Handler for Dapr Jobs
# The Dapr sidecar calls this method when the job fires.
# The URL convention for Dapr Jobs callback is often configurable or based on method invocation.
# However, standard Dapr Jobs often invoke specific methods on the app.
# Let's try to map it to /job/<name> or see if we can use a generic entry point.
# According to Dapr docs, the sidecar invokes `POST /job/<job_name>`.
# So we need a dynamic route or specific route.

@app.post("/job/{job_name}")
async def handle_job_callback(job_name: str, payload: dict): # Payload might be wrapped
    logger.info(f"⏰ JOB FIRED: {job_name}")
    
    # Payload from Dapr might be the 'data' we sent, or wrapped.
    # Usually it's the data object.
    # We sent a JSON string inside 'value' for google.protobuf.StringValue compatibility 
    # if using SDK, but here we used raw JSON.
    # Let's inspect payload.
    logger.info(f"Payload: {payload}")
    
    try:
        # Extract data
        # If we sent raw JSON as data, it might come as is.
        # But based on the code above:
        # "data": { "@type": ..., "value": json_string }
        # So payload might have that structure.
        
        inner_data = payload.get("value")
        if inner_data:
            import json
            data = json.loads(inner_data)
            title = data.get("title")
            user_id = data.get("user_id")
            logger.info(f"⏰ REMINDER: Task '{title}' is due now for user {user_id}!")
        else:
            # Fallback if structure is different
            logger.info(f"⏰ REMINDER: Job {job_name} fired (could not parse details)")
            
    except Exception as e:
        logger.error(f"Error processing job callback: {e}")

    return {}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)