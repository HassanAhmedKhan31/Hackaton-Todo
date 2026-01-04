# Task ID: T-002, T-003
from typing import List, Optional
from models import Task

class TodoService:
    """
    Service class to handle core and extended business logic for Todo tasks.
    """
    def __init__(self) -> None:
        self.tasks: List[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: str) -> Task:
        """
        Adds a new task to the in-memory list with an auto-incrementing ID.
        """
        new_task = Task(id=self._next_id, title=title, description=description)
        self.tasks.append(new_task)
        self._next_id += 1
        return new_task

    def list_tasks(self) -> List[Task]:
        """
        Returns the list of all tasks.
        """
        return self.tasks

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Finds a specific task by its ID.
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def delete_task(self, task_id: int) -> bool:
        """
        Removes a task from the list. Returns True if successful, False if not found.
        """
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """
        Updates task fields if provided. Returns the updated task or None if not found.
        """
        task = self.get_task(task_id)
        if task:
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            return task
        return None

    def complete_task(self, task_id: int) -> Optional[Task]:
        """
        Marks a task as 'completed'. Returns the updated task or None if not found.
        """
        task = self.get_task(task_id)
        if task:
            task.status = "completed"
            return task
        return None

if __name__ == "__main__":
    service = TodoService()
    
    # Test Add
    print("Adding task...")
    t1 = service.add_task("Buy groceries", "Milk, Eggs, Bread")
    print(f"Added: {t1}")
    
    # Test List
    print(f"All tasks: {service.list_tasks()}")
    
    # Test Update
    print("Updating task...")
    updated = service.update_task(1, title="Buy groceries today")
    print(f"Updated: {updated}")
    
    # Test Complete
    print("Completing task...")
    completed = service.complete_task(1)
    print(f"Completed: {completed}")
    
    # Test Delete
    print("Deleting task...")
    success = service.delete_task(1)
    print(f"Deleted successfully: {success}")
    print(f"Final task list: {service.list_tasks()}")