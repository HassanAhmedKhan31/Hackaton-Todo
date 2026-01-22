# Task ID: T-018-AI-Actions
from typing import Any, Dict, List
from sqlmodel import Session
from backend.database import engine
from backend.service import TodoService
from backend.models import Task

class TodoMCP:
    def get_tools(self) -> List[Dict[str, Any]]:
        """
        Returns the JSON Schema definitions for the tools.
        Compatible with OpenAI function calling format.
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task to the todo list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "The title of the task"},
                            "description": {"type": "string", "description": "Optional description"}
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List all tasks, optionally filtered by status",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "enum": ["pending", "completed"], "description": "Filter by status"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update a task's title, description, or status",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "integer", "description": "The ID of the task"},
                            "title": {"type": "string", "description": "New title"},
                            "description": {"type": "string", "description": "New description"},
                            "status": {"type": "string", "enum": ["pending", "completed"], "description": "New status"}
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task by ID",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "integer", "description": "The ID of the task"}
                        },
                        "required": ["task_id"]
                    }
                }
            }
        ]

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """
        Executes the tool with the given arguments.
        Returns the result (Pydantic model or list).
        """
        with Session(engine) as session:
            if name == "add_task":
                return TodoService.create_task(
                    session, 
                    title=arguments.get("title"), 
                    description=arguments.get("description")
                )
            elif name == "list_tasks":
                return TodoService.get_tasks(
                    session, 
                    status=arguments.get("status")
                )
            elif name == "update_task":
                # Handles generic updates (title, desc, status)
                task_id = arguments.get("task_id")
                if isinstance(task_id, str) and task_id.isdigit():
                    task_id = int(task_id)
                
                return TodoService.update_task(
                    session, 
                    task_id=task_id, 
                    title=arguments.get("title"),
                    description=arguments.get("description"),
                    status=arguments.get("status")
                )
            elif name == "complete_task":
                # Kept for backward compatibility if the AI tries to use it
                task_id = arguments.get("task_id")
                if isinstance(task_id, str) and task_id.isdigit():
                    task_id = int(task_id)
                return TodoService.update_task(session, task_id=task_id, status="completed")
            elif name == "delete_task":
                task_id = arguments.get("task_id")
                if isinstance(task_id, str) and task_id.isdigit():
                    task_id = int(task_id)
                return TodoService.delete_task(session, task_id=task_id)
            else:
                raise ValueError(f"Unknown tool: {name}")