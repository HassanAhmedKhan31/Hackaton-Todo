# Feature: Local Kubernetes Deployment (Phase IV)

## Requirements
1. **Containerization:**
   - Create `Dockerfile` for Backend (Python/FastAPI).
   - Create `Dockerfile` for Frontend (Next.js).
   - Use `.dockerignore` to keep images small.
2. **Orchestration (Kubernetes):**
   - Create Kubernetes manifests (Deployment, Service, Ingress) for both apps.
   - Use **Helm Charts** to package the application.
3. **Local Deployment:**
   - Deploy everything to **Minikube**.
   - Ensure Frontend can talk to Backend within the cluster.
   - Ensure Backend can talk to the external Neon DB.