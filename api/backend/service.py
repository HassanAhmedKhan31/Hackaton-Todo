# Task ID: T-012 (Refactoring for Shared Logic)
from typing import List, Optional
from sqlmodel import Session, select
from backend.models import Task

class TodoService:
    @staticmethod
    def create_task(session: Session, title: str, description: Optional[str] = None, user_id: Optional[str] = None, is_recurring: bool = False, recurrence_interval: Optional[str] = None, remind_at: Optional[str] = None) -> Task:
        task = Task(title=title, description=description, user_id=user_id, is_recurring=is_recurring, recurrence_interval=recurrence_interval, remind_at=remind_at)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_tasks(session: Session, status: Optional[str] = None) -> List[Task]:
        statement = select(Task)
        if status:
            statement = statement.where(Task.status == status)
        return session.exec(statement).all()

    @staticmethod
    def get_task(session: Session, task_id: int) -> Optional[Task]:
        return session.get(Task, task_id)

    @staticmethod
    def update_task(session: Session, task_id: int, status: Optional[str] = None, title: Optional[str] = None, description: Optional[str] = None, is_recurring: Optional[bool] = None, recurrence_interval: Optional[str] = None, remind_at: Optional[str] = None) -> Optional[Task]:
        task = session.get(Task, task_id)
        if not task:
            return None
        
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status
        if is_recurring is not None:
            task.is_recurring = is_recurring
        if recurrence_interval is not None:
            task.recurrence_interval = recurrence_interval
        if remind_at is not None:
            task.remind_at = remind_at
            
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete_task(session: Session, task_id: int) -> bool:
        task = session.get(Task, task_id)
        if not task:
            return False
        session.delete(task)
        session.commit()
        return True
