# Hackathon Todo: AI-Powered Task Manager

Welcome to **Hackathon Todo**, a cutting-edge task management application built for the Modern AI Agent Hackathon. This project demonstrates a progression from a simple service to a full-stack application, culminating in an AI-powered agentic workflow.

## Features

### Phase I: Core Service
- **Service Layer:** robust Python business logic for task management.
- **In-Memory Storage:** Initial prototyping with efficient data structures.
- **CLI Interface:** Basic command-line interaction for testing core logic.

### Phase II: Full Stack Web App
- **Modern Frontend:** Built with **Next.js**, utilizing React Server Components and Tailwind CSS for a sleek UI.
- **Robust Backend:** Powered by **FastAPI** for high-performance asynchronous API endpoints.
- **Database:** **Neon (PostgreSQL)** integration via **SQLModel** for reliable data persistence.
- **CRUD Operations:** Complete Create, Read, Update, Delete functionality exposed via RESTful APIs.

### Phase III: AI Agents
- **AI Integration:** Leverages **OpenAI** (or OpenRouter) models to understand natural language.
- **Model Context Protocol (MCP):** Implements an MCP server to standardize tool usage for the AI.
- **Chat Interface:** A dedicated chat UI where users can manage tasks conversationally (e.g., "Add a meeting with John tomorrow at 2 PM").
- **Agentic Workflow:** The AI autonomously calls backend tools to modify the database based on user intent.

## Tech Stack

- **Frontend:** Next.js (React), TypeScript, Tailwind CSS
- **Backend:** FastAPI, Python 3.10+
- **Database:** Neon (PostgreSQL), SQLModel (ORM)
- **AI/ML:** OpenAI API, Model Context Protocol (MCP)

## Setup Guide

Follow these steps to get the application running locally.

### Prerequisites
- Node.js (v18+)
- Python (v3.10+)
- A Neon PostgreSQL database URL
- An OpenAI API Key

### 1. Backend Setup

Navigate to the project root (or `backend` if you prefer separating environments, but `pyproject.toml` is in root).

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install fastapi "uvicorn[standard]" sqlmodel openai mcp python-dotenv psycopg2-binary
```

Create a `.env` file in the `backend/` directory (or root, depending on where you run it) with your credentials:

```env
DATABASE_URL=postgresql://user:password@ep-host.region.aws.neon.tech/neondb?sslmode=require
OPENAI_API_KEY=sk-...
```

Run the server:

```bash
# From the project root, assuming main.py is in backend/
uvicorn backend.main:app --reload
```
The API will be available at `http://localhost:8000`.

### 2. Frontend Setup

Open a new terminal and navigate to the `frontend` directory:

```bash
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

The application will be available at `http://localhost:3000`.

## Project Structure

```
├── backend/            # FastAPI application & MCP Server
│   ├── main.py         # App entry point
│   ├── agent.py        # AI Agent logic
│   ├── mcp/            # Model Context Protocol implementation
│   └── routes/         # API & Chat endpoints
├── frontend/           # Next.js application
│   ├── app/            # App Router pages
│   └── components/     # React components (ChatInterface, TodoApp)
├── specs/              # Documentation & Specifications (SDD)
└── pyproject.toml      # Python dependencies
```

## Status
**COMPLETE**
This project was successfully implemented following Spec-Driven Development (SDD) principles.
"# Hackaton-Todo" 
