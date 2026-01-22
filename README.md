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

### Phase IV: Containerization & Orchestration
- **Dockerized Services:** All components (Frontend, Backend, and microservices) are containerized for consistent deployment.
- **Kubernetes (K8s):** Deployed on Kubernetes (Minikube locally, DOKS in cloud) for scalability and management.
- **Helm Charts:** Infrastructure as Code (IaC) using Helm to manage deployments, services, and configuration.

### Phase V: Cloud-Native Architecture
- **Event-Driven Design:** Utilizes **Dapr (Distributed Application Runtime)** and **Kafka** for asynchronous communication between services.
- **Microservices Pattern:** Broken down into specialized services:
    - **Backend API:** Core logic and data access.
    - **Notification Service:** Consumes events to handle alerts and scheduled reminders (via Dapr Jobs).
    - **Recurring Service:** "Brain" that autonomously reschedules tasks upon completion.
- **Cloud Deployment:** Fully deployed to **DigitalOcean Kubernetes (DOKS)** with CI/CD via **GitHub Actions**.
- **Observability:** Distributed tracing enabled with **Zipkin** to visualize service-to-service calls.

## Tech Stack

- **Frontend:** Next.js (React), TypeScript, Tailwind CSS
- **Backend:** FastAPI, Python 3.10+, Dapr SDK
- **Database:** Neon (PostgreSQL), SQLModel (ORM)
- **Messaging/Integration:** Dapr, Apache Kafka
- **Infrastructure:** Docker, Kubernetes (DOKS), Helm
- **CI/CD:** GitHub Actions
- **AI/ML:** OpenAI API, Model Context Protocol (MCP)

## Project Structure

```
├── backend/                  # Core Backend Service
│   ├── main.py               # App entry point
│   ├── agent.py              # AI Agent logic
│   ├── mcp/                  # Model Context Protocol
│   ├── routes/               # API Endpoints
│   ├── notification_service/ # [New] Notification & Scheduler Microservice
│   └── recurring_service/    # [New] Recurring Task Automation Microservice
├── frontend/                 # Next.js Application
│   ├── app/                  # App Router
│   └── components/           # UI Components
├── k8s/                      # Kubernetes Manifests & Helm Charts
│   ├── hackathon-todo/       # Main Helm Chart
│   └── kafka-fix.yaml        # Kafka Configuration
├── .github/workflows/        # CI/CD Pipelines
└── specs/                    # Documentation & Specifications
```

## Setup Guide

### Local Development (Minikube)

1.  **Start Minikube with Dapr:**
    ```bash
    minikube start --cpus 4 --memory 8192
    dapr init -k
    ```
2.  **Deploy Kafka:**
    ```bash
    kubectl apply -f k8s/kafka-fix.yaml
    ```
3.  **Build Images:**
    ```bash
    eval $(minikube docker-env)
    docker build -t hackathon-backend:latest ./backend
    docker build -t hackathon-frontend:latest ./frontend
    docker build -t notification-service:latest ./backend/notification_service
    docker build -t recurring-service:latest ./backend/recurring_service
    ```
4.  **Install Chart:**
    ```bash
    helm install hackathon-todo ./k8s/hackathon-todo
    ```
5.  **Access:**
    - **Frontend:** `minikube service hackathon-todo-frontend` (or via Ingress/Tunnel)

### Cloud Deployment (DOKS)

The project is configured for automated deployment via GitHub Actions.
1.  **Secrets:** Configure `DOCKERHUB_USERNAME`, `DIGITALOCEAN_ACCESS_TOKEN`, `DATABASE_URL`, etc., in GitHub.
2.  **Push:** Commit to `main` to trigger the pipeline.
3.  **Access:** The application is available at the configured Ingress URL (e.g., `http://todo.yourdomain.com`).

## Status
**COMPLETE**
This project was successfully implemented following Spec-Driven Development (SDD) principles and has achieved **Level 5: Cloud-Native Mastery**.
"# Hackaton-Todo" 
"# Hackaton-Todo-Project" 
