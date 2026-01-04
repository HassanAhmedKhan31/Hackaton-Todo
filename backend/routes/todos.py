# Task ID: T-008, T-012
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from backend.database import get_session
from backend.models import Task
from backend.service import TodoService

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=Task)
def create_task(task: Task, session: Session = Depends(get_session)):
    """Create a new task."""
    return TodoService.create_task(session, title=task.title, description=task.description)

@router.get("/", response_model=List[Task])
def read_tasks(session: Session = Depends(get_session)):
    """Read all tasks."""
    return TodoService.get_tasks(session)

@router.get("/{task_id}", response_model=Task)
def read_task(task_id: int, session: Session = Depends(get_session)):
    """Read a specific task."""
    task = TodoService.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: Task, session: Session = Depends(get_session)):
    """Update a task."""
    task = TodoService.update_task(
        session, 
        task_id=task_id, 
        title=task_data.title, 
        description=task_data.description, 
        status=task_data.status
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    """Delete a task."""
    success = TodoService.delete_task(session, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"ok": True}
