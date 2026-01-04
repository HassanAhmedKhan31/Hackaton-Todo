# Tasks

## Phase II: Full-Stack Web App (FastAPI + Next.js + Database)

### Task ID: T-006 [COMPLETED]
**Objective:** Project Restructure for Phase II.
**Files:** `backend/`, `archive/`
**Description:** Create an `archive/` folder. Move all Phase I `src/` files (`models.py`, `service.py`, `ui.py`, `main.py`) into `archive/`. Ensure the `backend/` folder is ready.
**Verification:** Run `ls -R archive/` to confirm files are moved and `ls src/` is empty (or removed).

### Task ID: T-007 [COMPLETED]
**Objective:** Database & SQLModel Setup.
**Files:** `backend/database.py`, `backend/models.py`
**Description:** 
1. Install `sqlmodel` and `uvicorn[standard]` (and `fastapi`).
2. Create `backend/models.py`: Define `Task` as a `SQLModel, table=True`.
3. Create `backend/database.py`: Setup `create_engine` (using SQLite for dev simplicity first, or connect to Neon if URL provided) and a `get_session` dependency.
**Verification:** Run a script that imports `engine` and calls `SQLModel.metadata.create_all(engine)` to create the table locally.

### Task ID: T-008 [COMPLETED]
**Objective:** API Development (FastAPI Routes).
**Files:** `backend/main.py`, `backend/api.py` (or routes/todos.py)
**Description:**
1. Create `backend/main.py` to initialize `FastAPI`.
2. Implement CRUD routes: `GET /tasks`, `POST /tasks`, `PUT /tasks/{id}`, `DELETE /tasks/{id}`.
3. Use `Session = Depends(get_session)` to interact with the DB.
**Verification:** Run `uvicorn backend.main:app --reload`. Use `curl` or Swagger UI (`/docs`) to Add and List tasks.

### Task ID: T-009 [COMPLETED]
**Objective:** Frontend Setup (Next.js).
**Files:** `frontend/package.json`
**Description:** Initialize a new Next.js app in `frontend/`. Use TypeScript, Tailwind CSS, App Router. (e.g., `npx create-next-app@latest frontend`).
**Verification:** Run `npm run dev` in `frontend/` and access `http://localhost:3000`.

### Task ID: T-010 [COMPLETED]
**Objective:** Frontend UI & Integration.
**Files:** `frontend/src/app/page.tsx`, `frontend/src/components/TaskList.tsx`
**Description:**
1. Create a `TaskList` component that fetches data from `http://localhost:8000/tasks`.
2. Create an "Add Task" form.
3. Update `page.tsx` to display the list and form.
**Verification:** Open the browser. Add a task via the UI. Refresh. Ensure the task persists (fetch from Backend DB).

## Phase III: AI Chatbot Integration

### Task ID: T-011 [COMPLETED]
**Objective:** Backend Dependencies & Configuration.
**Files:** `pyproject.toml`, `.env`
**Description:**
1. Add `openai` and `mcp` to `pyproject.toml`.
2. Update `.env` to include `OPENAI_API_KEY`.
3. Install the new dependencies.
**Verification:** Run `pip list` to confirm `openai` and `mcp` are installed.

### Task ID: T-012 [COMPLETED]
**Objective:** MCP Server & Tool Definitions.
**Files:** `backend/mcp/server.py`, `backend/mcp/tools.py`
**Description:**
1. Create `backend/mcp/tools.py`: Implement wrapper functions (`add_task`, `list_tasks`, `complete_task`, `delete_task`) that call `service.py`.
2. Create `backend/mcp/server.py`: Implement the MCP Server class and register the Todo functions from `tools.py` as Tools.
**Verification:** Verify the server script can be imported or run without syntax errors.

### Task ID: T-013 [COMPLETED]
**Objective:** AI Agent Logic.
**Files:** `backend/agent.py`
**Description:**
1. Create `backend/agent.py`.
2. Initialize the OpenAI Agent.
3. Connect the Agent to the MCP Server tools defined in T-012.
**Verification:** Create a simple test script to instantiate the Agent and verify it sees the tools.

### Task ID: T-014 [COMPLETED]
**Objective:** Chat API Endpoint.
**Files:** `backend/routes/chat.py`, `backend/main.py`
**Description:**
1. Create `backend/routes/chat.py`: Implement the `POST /api/chat` endpoint.
2. The endpoint receives a user message, passes it to the Agent, and returns the response.
3. Register the new router in `backend/main.py`.
**Verification:** Send a `POST /api/chat` request with a message and verify a response is returned.

### Task ID: T-015 [COMPLETED]
**Objective:** Frontend Chat Interface.
**Files:** `frontend/package.json`, `frontend/src/components/ChatInterface.tsx`, `frontend/src/app/page.tsx`
**Description:**
1. Install OpenAI ChatKit (or equivalent AI UI library) in the frontend.
2. Create `frontend/src/components/ChatInterface.tsx` that talks to `POST /api/chat`.
3. Add the chat component to `frontend/src/app/page.tsx`.
**Verification:** Use the web UI to chat with the bot and verify it can manage tasks (add/list/complete).

## Finalization

### Task ID: T-FINAL [COMPLETED]
**Objective:** Project Documentation & Cleanup.
**Files:** `README.md`
**Description:**
1. Overwrite `README.md` with a professional Hackathon submission document.
2. List Features (Phase I, II, III), Tech Stack, and Setup Guide.
3. Clean up temporary test files.
**Verification:** Check `README.md` content and ensure project directory is clean.

## Phase IV: Containerization & Kubernetes

### Task ID: T-016 [COMPLETED]
**Objective:** Containerize Backend and Frontend (Dockerfiles).
**Files:** `backend/Dockerfile`, `frontend/Dockerfile`, `backend/.dockerignore`, `frontend/.dockerignore`
**Description:**
1. Create `backend/Dockerfile`: Configure for production using `python:3.11-slim`.
2. Create `frontend/Dockerfile`: Configure for production using multi-stage builds.
3. Create `.dockerignore` files.
**Verification:** Run `docker build` commands successfully.

### Task ID: T-017 [COMPLETED]
**Objective:** Build Automation Script.
**Files:** `scripts/build_images.ps1`
**Description:**
1. Create `scripts/build_images.ps1` (PowerShell script for Windows).
2. The script should build and tag the backend and frontend images.
**Verification:** Run the script and verify images appear in `docker images`.

### Task ID: T-018 [COMPLETED]
**Objective:** Kubernetes Helm Chart.
**Files:** `k8s/hackathon-todo/Chart.yaml`, `k8s/hackathon-todo/values.yaml`, `k8s/hackathon-todo/templates/`
**Description:**
1. Create a Helm Chart in `k8s/hackathon-todo/`.
2. Create templates for Deployment (Backend & Frontend).
3. Create templates for Service (ClusterIP for Backend, LoadBalancer/NodePort for Frontend).
4. Create templates for Secrets (for `DATABASE_URL` and `OPENAI_API_KEY`).
**Verification:** Run `helm template ./k8s/hackathon-todo` to verify syntax and output.

### Task ID: T-019 [COMPLETED]
**Objective:** Deploy to Minikube.
**Files:** `k8s/`
**Description:**
1. Deploy the Helm chart to the local Minikube cluster.
2. Ensure images are available to Minikube (e.g., via `minikube docker-env` or loading images).
**Verification:** Run `kubectl get pods` to see them running.

### Task ID: T-020
**Objective:** Verification.
**Files:** N/A
**Description:**
1. Verify the app runs on the Minikube IP.
2. Ensure Backend and Frontend communicate correctly in the cluster.
**Verification:** Access the application in the browser and perform a full integration test.

## Phase V: Advanced Cloud & Event-Driven Architecture

### Task ID: T-021
**Objective:** Install Dapr on Minikube.
**Files:** N/A (CLI Commands)
**Description:** Install Dapr CLI and initialize it in the Kubernetes cluster.
**Verification:** `kubectl get pods -n dapr-system` shows running pods.

### Task ID: T-022
**Objective:** Install Kafka (Strimzi) on Minikube.
**Files:** `k8s/kafka-cluster.yaml`
**Description:** Deploy the Strimzi Operator and a minimalistic Kafka cluster.
**Verification:** `kubectl get pods -n kafka` shows the Kafka cluster running.