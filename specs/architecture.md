# Architecture

## Overview
This document outlines the system architecture, evolving from a local CLI (Phase I) to a Full-Stack Web App (Phase II), an AI-Integrated System (Phase III), and finally a Cloud-Native Deployment (Phase IV).

## Phase II: Full-Stack Web App

### 1. Backend (`backend/`)
**Framework:** FastAPI (Python)
**Responsibilities:** API Endpoints, Business Logic, Database Access.
**Components:**
- `backend/models.py`: SQLModel database tables (`Task`).
- `backend/database.py`: DB Connection (Async Engine) using `SQLModel`.
- `backend/service.py`: CRUD logic using `AsyncSession`.
- `backend/api.py`: FastAPI Router (`/tasks`, `/tasks/{id}`).
- `backend/main.py`: App entry point.

### 2. Frontend (`frontend/`)
**Framework:** Next.js 14 (App Router), TypeScript, Tailwind CSS.
**Responsibilities:** User Interface, State Management, API Integration.
**Components:**
- `frontend/src/app/page.tsx`: Main dashboard.
- `frontend/src/components/`: Reusable UI components.
- `frontend/src/lib/api.ts`: Fetch wrapper for backend calls.

### 3. Database
**Provider:** Neon (PostgreSQL).
**ORM:** SQLModel.

---

## Phase III: AI Chatbot Integration

### 1. Frontend (`frontend/`)
**Component:** AI Chat Interface.
**Library:** OpenAI ChatKit (or compatible UI component).
**Responsibilities:**
- Display chat history.
- Send user messages to `POST /api/chat`.
- Render markdown/structured responses from the Agent.

### 2. Backend Extensions (`backend/`)

#### A. MCP Server & Tools (`backend/mcp/`)
**Role:** Exposes Todo domain logic as standard AI Tools.
**Protocol:** Model Context Protocol (MCP).
**Files:**
- `backend/mcp/server.py`: MCP Server instance.
- `backend/mcp/tools.py`: Tool definitions wrapping `service.py`.
    - `add_task(title, description)`
    - `list_tasks(status)`
    - `complete_task(task_id)`
    - `delete_task(task_id)`

#### B. AI Agent Endpoint (`backend/routes/chat.py`)
**Role:** Handles natural language requests.
**Endpoint:** `POST /api/chat`
**Logic:**
1.  Receives user message from Frontend.
2.  Initializes (or retrieves) an **OpenAI Agent**.
3.  **Tool Access:** The Agent is configured to use the tools defined in the MCP Server.
4.  **Execution:** The Agent reasons, calls MCP tools (which call `service.py`), and generates a response.
5.  **Response:** Returns the agent's text/actions to the Frontend.

### 3. Data Flow (AI Path)
1.  **User** types "Remind me to buy milk" in Frontend.
2.  **Frontend** sends POST to `backend/routes/chat.py`.
3.  **FastAPI** spins up AI Agent.
4.  **AI Agent** looks at available tools (MCP).
5.  **AI Agent** calls `add_task_tool("Buy milk")`.
6.  **MCP Tool** calls `service.create_task(...)`.
7.  **Service** writes to **PostgreSQL**.
8.  **Result** propagates back to User.

---

## Phase IV: Containerization & Kubernetes

### 1. Containerization (Docker)
**Strategy:** Multi-stage builds to minimize image size.

#### A. Backend (`backend/Dockerfile`)
- **Base Image:** `python:3.11-slim` (Lightweight Python).
- **Build Stage:** Install build dependencies, pip install requirements.
- **Run Stage:** Copy installed packages, copy source code.
- **Command:** `uvicorn backend.main:app --host 0.0.0.0 --port 8000`.

#### B. Frontend (`frontend/Dockerfile`)
- **Base Image:** `node:18-alpine`.
- **Build Stage:** `npm install`, `npm run build`.
- **Run Stage:** `npm start` (Production mode).
- **Env Vars:** `NEXT_PUBLIC_API_URL` (Needs to point to K8s Service/Ingress or localhost for Minikube forwarding).

### 2. Orchestration (Kubernetes via Helm)
**Tool:** Helm (Package Manager).
**Chart Structure:** `k8s/charts/hackathon-todo/` containing templates for both Backend and Frontend.

#### A. Backend Deployment
- **Kind:** `Deployment`.
- **Replicas:** 1 (configurable in `values.yaml`).
- **Env Vars:**
    - `DATABASE_URL`: Injected from K8s Secret.
    - `OPENAI_API_KEY`: Injected from K8s Secret.
- **Service:** ClusterIP (Port 8000).

#### B. Frontend Deployment
- **Kind:** `Deployment`.
- **Replicas:** 1.
- **Service:** NodePort or LoadBalancer (Port 3000) to expose to host.

#### C. Configuration Management
- **Secrets:** Kubernetes Secret object `hackathon-todo-secrets` created manually or via external-secrets (for this Hackathon, manual/script creation is acceptable).
- **Values:** `values.yaml` defines image repository, tag, and replica counts.

### 3. Deployment Flow (Minikube)
1.  **Build:** `eval $(minikube docker-env)` && `docker build ...` (Build images directly into Minikube's registry).
2.  **Secrets:** Create generic secret from `.env` file.
    - `kubectl create secret generic app-secrets --from-literal=DATABASE_URL=... --from-literal=OPENAI_API_KEY=...`
3.  **Install:** `helm install todo-app ./k8s/charts/hackathon-todo`.
4.  **Access:** `minikube service todo-frontend` to open in browser.
