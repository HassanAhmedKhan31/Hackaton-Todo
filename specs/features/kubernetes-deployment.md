# Feature: Local Kubernetes Deployment (Phase IV)

## 1. Goal
Deploy the existing "Hackathon Todo Chatbot" (Frontend + Backend + DB connection) to a local Kubernetes cluster (Minikube).
The application logic (Python/JS code) must NOT be modified.
Configuration (Environment Variables) must be injected via Kubernetes Secrets.

## 2. Requirements
- **Local Compatibility:** The deployment must run on Minikube.
- **Zero Code Change:** No changes to `backend/*.py` or `frontend/src/*`.
- **Secret Management:** Sensitive data (`OPENAI_API_KEY`, `DATABASE_URL`) must be mounted as environment variables.
- **Service Discovery:** Frontend must find Backend via K8s Service DNS (not localhost).
- **Persistence:** Connect to the existing Neon DB (external) or a local Postgres (if configured). *For this task, we will use the existing Neon DB connection string provided in .env.*

## 3. Architecture
- **Ingress:** Minikube Tunnel or NodePort for accessing Frontend.
- **Frontend Pod:** Next.js container. Connects to Backend Service.
- **Backend Pod:** FastAPI container. Connects to External DB (Neon).
- **Secrets:** Kubernetes Secret object holding `.env` values.

## 4. Plan
1.  **Containerization Verification:**
    - Verify `backend/Dockerfile` builds and runs.
    - Verify `frontend/Dockerfile` builds and runs.
2.  **Helm Chart Construction:**
    - Create/Refine `Chart.yaml`.
    - Define `values.yaml` for local configuration.
    - Create `templates/secrets.yaml` to map `.env` vars.
    - Create `templates/backend-deployment.yaml` and `service.yaml`.
    - Create `templates/frontend-deployment.yaml` and `service.yaml`.
3.  **Deployment & Validation:**
    - Build images (locally or in minikube env).
    - Install Helm Chart.
    - Port-forward or access via NodePort.

## 5. Tasks (Implementation Steps)
- [ ] **Task 1: Spec Creation** (This file).
- [ ] **Task 2: Dockerfile Review.** Ensure `uvicorn` and `next start` commands are correct.
- [ ] **Task 3: Helm Chart Generation.**
    - Define `values.yaml` with placeholders for keys.
    - Ensure `secrets.yaml` uses Base64 encoding or Helm string injection.
    - Ensure Backend Service is exposed on ClusterIP.
    - Ensure Frontend connects to `http://<backend-service-name>`.
- [ ] **Task 4: Environment Mapping.**
    - Map `DATABASE_URL` and `OPENAI_API_KEY` from local `.env` to the Helm install command.
