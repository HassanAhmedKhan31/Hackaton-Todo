# Hackathon Technical Documentation

---

### 1. Technical Summary: Solving Latency with BackgroundTasks and Polling

A key challenge in this project was the latency introduced by the AI Agent, which could take several seconds to process a new task. A naive implementation would block the API response until the AI processing was complete, leading to a frustrating user experience where the UI would freeze.

Our solution was a two-part strategy:

*   **Backend (FastAPI `BackgroundTasks`):** On the backend, we leveraged FastAPI's `BackgroundTasks` feature. When a user creates a task, the API endpoint immediately adds the long-running AI processing function to a background queue and returns a `201 CREATED` response to the client. This makes the initial API call feel instantaneous.

*   **Frontend (Polling & Optimistic UI):** On the frontend, we implemented a polling mechanism using a `useEffect` hook in our main `page.tsx` component. This hook re-fetches the full task list from the backend every 5 seconds. To enhance the user experience, a "Status: Processing..." label is shown for tasks that are still being updated by the AI. This combination ensures the UI remains responsive and the user receives near-real-time updates without needing to manually refresh the page.

---

### 2. Dynamic Schema Migration Strategy

During development, we needed to add new columns to our PostgreSQL database (e.g., `is_recurring`, `recurrence_interval`). To avoid manual database alterations and ensure smooth deployments, we implemented a dynamic schema migration strategy.

A Python script, `fix_schema.py`, was created to handle all database alterations. This script uses `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` SQL commands, which makes it safe to run multiple times without causing errors.

This `migrate()` function is called from within the FastAPI application's `lifespan` event handler in `main.py`. This ensures that every time the backend application starts up, it first checks and applies any necessary database schema changes before serving traffic. This automated approach makes the application resilient and simplifies the deployment process, as we no longer need to worry about the database being out of sync with the code.

---

### 3. Project Abstract

In an era where AI is transforming user experiences, integrating intelligent features without sacrificing performance is a critical challenge. This project presents a modern, microservices-based Todo application that successfully marries a responsive user interface with a powerful AI agent. Built with a Next.js frontend and a FastAPI backend, the application is orchestrated on Kubernetes to ensure scalability and resilience, making it ready for production workloads.

Our key innovation lies in the architectural approach to handling long-running, asynchronous operations. By leveraging FastAPI's built-in `BackgroundTasks` and a frontend polling mechanism, we delegate time-consuming AI processing to a non-blocking background queue. This allows the user to continue interacting with the application without any perceived latency, while the AI agent intelligently enriches task data in the background. The result is a seamless and fluid user experience that masks the complexity of the distributed system. This project serves as a blueprint for building high-performance, AI-driven applications using modern cloud-native principles, demonstrating that intelligence and speed can coexist.

---

### 4. Future Enhancements

The current implementation includes a database foundation for more advanced features, which opens up several exciting possibilities for future development.

*   **Automated Recurring Tasks:** The database schema already includes an `is_recurring` boolean field and a `recurrence_interval` string (e.g., "daily", "weekly"). A new microservice could be developed to act as a scheduler. This service would run on a cron-like schedule (e.g., once every hour), scan the database for tasks marked as recurring, and automatically re-add them to the user's active task list based on their specified interval.

*   **Proactive Notifications:** The `remind_at` timestamp field could be used to build a proactive notification system. The scheduler service could also be responsible for checking for upcoming deadlines and sending notifications to users via a service like Twilio for SMS or an email delivery API. This would transform the application from a passive list-keeper into an active assistant that helps users stay on top of their commitments.
