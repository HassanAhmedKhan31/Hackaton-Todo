# Task ID: T-008
from typing import Optional
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