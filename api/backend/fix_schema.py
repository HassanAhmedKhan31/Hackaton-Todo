from sqlalchemy import text
from backend.database import engine

def migrate():
    with engine.connect() as conn:
        print("Adding is_recurring...")
        try:
            conn.execute(text('ALTER TABLE task ADD COLUMN IF NOT EXISTS is_recurring BOOLEAN DEFAULT FALSE;'))
        except Exception as e:
            print(f"Skipped is_recurring: {e}")

        print("Adding recurrence_interval...")
        try:
            conn.execute(text('ALTER TABLE task ADD COLUMN IF NOT EXISTS recurrence_interval VARCHAR;'))
        except Exception as e:
            print(f"Skipped recurrence_interval: {e}")

        print("Adding remind_at...")
        try:
            conn.execute(text('ALTER TABLE task ADD COLUMN IF NOT EXISTS remind_at TIMESTAMP;'))
        except Exception as e:
            print(f"Skipped remind_at: {e}")
            
        conn.commit()
        print("Schema update complete.")

if __name__ == "__main__":
    migrate()