# Feature: Full-Stack Web Implementation (Phase II)

## Requirements
1. **API Layer (FastAPI):**
   - Expose the TodoService as REST endpoints (GET, POST, PUT, DELETE).
   - Use SQLModel to talk to a real PostgreSQL database.
2. **Frontend Layer (Next.js):**
   - Create a clean UI to display and manage tasks.
   - Connect to the FastAPI backend.
3. **Database:**
   - Tasks must persist in Neon DB (not in memory).
   - Table Schema: `id`, `title`, `description`, `status`.