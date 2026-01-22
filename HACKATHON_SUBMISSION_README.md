# Hackathon Submission: Event-Driven Todo App

This project is a modern, event-driven Todo application built for performance and scalability. It features a FastAPI backend, a React-based frontend, and leverages AI for intelligent task processing. The entire application is containerized and designed for cloud-native deployment.

## Key Features

- **Asynchronous Task Processing:** AI-powered task enrichment runs in the background, ensuring immediate UI feedback.
- **Event-Driven Architecture:** Microservices communicate through Kafka, enabling a decoupled and scalable system.
- **Automated Migrations:** Database schema migrations are handled automatically on startup.
- **Containerized Deployment:** The application is fully containerized with Docker and orchestrated with Kubernetes.
- **Live on Vercel:** The production environment is deployed on Vercel, with local development managed by Minikube.

## Technical Deep Dive

### Solving Latency with Background Tasks

A major challenge with integrating AI into a user-facing application is the potential for high latency. AI models can take several seconds—or even minutes—to return a response. To solve this, we used FastAPI's `BackgroundTasks`.

When a user creates a new task, the API endpoint immediately adds the task to the database and returns a response to the client. The long-running AI processing (which enriches the task with more details) is passed to a background task. This makes the UI feel instantaneous.

The frontend is designed to poll for updates every few seconds. This ensures that as soon as the AI agent finishes its work, the new information is reflected in the UI without requiring a manual refresh. This architecture is key to moving from a multi-minute delay to sub-second UI updates.

### Automated Schema Migrations with `fix_schema.py`

Database schema management is a common challenge in evolving applications. For this project, we implemented a simple and effective migration strategy using a Python script, `fix_schema.py`.

This script is executed every time the application starts up. It uses `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` commands to add new columns to the database. This approach has several advantages:

- **Idempotent:** The script can be run multiple times without causing errors.
- **Simple:** It's easy to add new migrations.
- **Automated:** No manual intervention is required to update the database schema.

This ensures that the database is always in sync with the application code, which is especially useful in a containerized environment where services might be restarted or scaled independently.

## Deployment

The application is designed for a hybrid deployment model:

- **Local Development:** We use Minikube to run a local Kubernetes cluster. This allows us to test the full, containerized application on a local machine.
- **Production:** The application is deployed to Vercel. The frontend is served by Vercel's CDN, and the backend services are run as Vercel Functions. The event-driven architecture with Kafka ensures that our background processing can scale independently of the user-facing API.
