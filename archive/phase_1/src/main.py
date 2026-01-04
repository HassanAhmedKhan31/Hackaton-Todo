# Task ID: T-005
import sys
from service import TodoService
from ui import TodoUI

def main() -> None:
    """
    Application entry point. Initializes services and starts the UI loop.
    """
    service = TodoService()
    ui = TodoUI(service)

    print("Welcome to the Hackathon Todo App!")

    while True:
        ui.show_menu()
        choice = input("\nSelect an option (1-6): ").strip()

        if choice == "1":
            ui.add_task_ui()
        elif choice == "2":
            ui.list_tasks_ui()
        elif choice == "3":
            ui.update_task_ui()
        elif choice == "4":
            ui.delete_task_ui()
        elif choice == "5":
            ui.complete_task_ui()
        elif choice == "6":
            print("Exiting application. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Exiting...")
        sys.exit(0)
