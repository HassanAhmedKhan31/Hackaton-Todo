# Task ID: T-016
# Use python:3.11-slim as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
# We copy the current directory (backend/) into /app/backend/ 
# because the code uses 'from backend.database ...'
COPY . ./backend/

# Copy the schema migration script
COPY fix_schema.py .

# Expose port
EXPOSE 8000

# Run uvicorn
CMD ["uvicorn", "backend.main:root_app", "--host", "0.0.0.0", "--port", "8000"]
