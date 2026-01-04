# Backend Guidelines (Phase III: AI Integration)

## Core Stack
- **FastAPI**: API Framework.
- **SQLModel**: ORM (PostgreSQL via Neon).
- **OpenAI Agent**: AI reasoning.
- **MCP (Model Context Protocol)**: Standardized tool interface.

## AI Dependencies
- `openai`: For LLM interaction.
- `mcp`: For exposing domain tools to the Agent.
- `python-dotenv`: For managing environment variables.

## Project Structure
- `backend/mcp/`: MCP Server and Tool definitions.
- `backend/routes/`: FastAPI routers (including `chat.py`).
- `backend/service.py`: Business logic (shared by API and AI).

## Commands
- Run server: `uvicorn backend.main:app --reload`
- Test AI Env: `python backend/test_ai_env.py`
