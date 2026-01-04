# Task ID: T-007
import os
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel, Session

# Load environment variables
load_dotenv()

# Get Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")

# Create engine
# Define connection args based on DB type
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
else:
    # POSTGRES FIX: Keep connection alive to prevent SSL drops
    connect_args = {
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5
    }

# Create Engine with pool_pre_ping=True
# This automatically reconnects if the DB connection is lost
engine = create_engine(
    DATABASE_URL, 
    connect_args=connect_args, 
    pool_pre_ping=True
)

def get_session():
    """Dependency for getting a database session."""
    with Session(engine) as session:
        yield session

def init_db():
    """Initializes the database tables."""
    SQLModel.metadata.create_all(engine)