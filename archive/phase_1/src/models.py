# Task ID: T-001
from dataclasses import dataclass

@dataclass
class Task:
    """
    Represents a task in the system.
    """
    id: int
    title: str
    description: str
    status: str = "pending"  # Default status is 'pending'
