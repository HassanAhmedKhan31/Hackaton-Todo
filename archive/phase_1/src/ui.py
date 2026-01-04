# Task ID: T-004
import sys
from typing import Optional
from service import TodoService

class TodoUI:
    """
    Handles user interaction for the Todo application.
    """
    def __init__(self, service: TodoService) -> None:
        self.service = service

    def show_menu(self) -> None:
        """Displays the main menu options."""
        print("\n--- Todo App Menu ---")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Complete Task")
        print("6. Exit")

    def get_input(self, prompt: str) -> str:
        """Wrapper for input to make it mockable if needed."""
        return input(prompt).strip()

    def add_task_ui(self) -> None:
        print("\n--- Add Task ---")
        title = self.get_input("Enter title: ")
        if not title:
            print("Title cannot be empty.")
            return
        description = self.get_input("Enter description: ")
        task = self.service.add_task(title, description)
        print(f"Task added successfully! ID: {task.id}")

    def list_tasks_ui(self) -> None:
        print("\n--- All Tasks ---")
        tasks = self.service.list_tasks()
        if not tasks:
            print("No tasks found.")
            return
        for task in tasks:
            print(f"[{task.id}] {task.title} - {task.status}")
            print(f"    Description: {task.description}")

    def update_task_ui(self) -> None:
        print("\n--- Update Task ---")
        try:
            task_id = int(self.get_input("Enter Task ID to update: "))
        except ValueError:
            print("Invalid ID.")
            return

        print("Leave blank to keep current value.")
        title = self.get_input("New title: ") or None
        description = self.get_input("New description: ") or None

        updated_task = self.service.update_task(task_id, title, description)
        if updated_task:
            print("Task updated successfully.")
        else:
            print("Task not found.")

    def delete_task_ui(self) -> None:
        print("\n--- Delete Task ---")
        try:
            task_id = int(self.get_input("Enter Task ID to delete: "))
        except ValueError:
            print("Invalid ID.")
            return

        if self.service.delete_task(task_id):
            print("Task deleted successfully.")
        else:
            print("Task not found.")

    def complete_task_ui(self) -> None:
        print("\n--- Complete Task ---")
        try:
            task_id = int(self.get_input("Enter Task ID to complete: "))
        except ValueError:
            print("Invalid ID.")
            return

        completed_task = self.service.complete_task(task_id)
        if completed_task:
            print(f"Task {task_id} marked as completed.")
        else:
            print("Task not found.")

if __name__ == "__main__":
    # Simple verification that class instantiates
    s = TodoService()
    ui = TodoUI(s)
    ui.show_menu()
    print("UI Module loaded successfully.")
