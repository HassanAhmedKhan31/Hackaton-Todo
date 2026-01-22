import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import sys

def cleanup_tasks():
    """Connects to the database and truncates the task table."""
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Get the database URL from the environment, ensuring it's set
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("🔴 ERROR: DATABASE_URL environment variable is not set.", file=sys.stderr)
        print("Please create a .env file or set the variable manually.", file=sys.stderr)
        sys.exit(1)

    print(f"Connecting to database...")

    try:
        # Create a database engine
        engine = create_engine(db_url)
        
        # Connect and execute the truncate command
        with engine.connect() as connection:
            print("Truncating 'task' table to reset data...")
            # Use a transaction to ensure atomicity
            with connection.begin():
                # TRUNCATE is efficient and resets the ID counter
                connection.execute(text("TRUNCATE TABLE task RESTART IDENTITY CASCADE;"))
            print("✅ Success! All tasks have been deleted and the ID counter is reset.")
            
    except Exception as e:
        print(f"🔴 ERROR: An error occurred while trying to clean the database.", file=sys.stderr)
        print(f"Error details: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    # Ask for user confirmation
    confirm = input("⚠️ This will permanently delete ALL tasks. Are you sure? (y/n): ")
    if confirm.lower() == 'y':
        cleanup_tasks()
    else:
        print("Cleanup cancelled.")