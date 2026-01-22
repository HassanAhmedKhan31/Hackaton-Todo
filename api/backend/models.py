# Task ID: T-008
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    """
    SQLModel representation of the Task table.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    status: str = Field(default="pending")
    user_id: Optional[str] = Field(default=None) # Added for future auth
    is_recurring: bool = Field(default=False)
    recurrence_interval: Optional[str] = Field(default=None) # e.g., "daily", "weekly"
    remind_at: Optional[datetime] = Field(default=None) # ISO 8601 datetime