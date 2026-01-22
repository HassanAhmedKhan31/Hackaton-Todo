## Architecture Data Flow

Our application follows a modern, decoupled architecture that ensures scalability and a responsive user experience. Here's a high-level overview of the data flow:

1.  **Frontend (React on Vercel):** The user interacts with our web application, built with React and hosted on Vercel. When a user submits a new Todo, the frontend sends a request to our FastAPI backend.

2.  **Backend (FastAPI on Vercel):** The FastAPI backend receives the request. It immediately writes the new task to our Neon Database and sends a response back to the frontend. This makes the initial UI update feel instant.

3.  **Asynchronous AI Processing:** The "magic" happens in the background. The FastAPI endpoint triggers a background task that sends the Todo item to an AI agent powered by OpenRouter. This agent processes the natural language input and generates a structured Todo item with additional details.

4.  **Database (Neon DB):** The Neon Database is our single source of truth. It's a serverless PostgreSQL database that's highly scalable and resilient. Both the initial task creation and the updates from the AI agent are persisted here.

5.  **UI Updates:** The frontend is configured to poll the backend for new data every few seconds. As soon as the AI agent has updated the task in the database, the new information automatically appears in the UI.

This architecture allows us to provide a fast, seamless user experience while leveraging powerful AI capabilities that would otherwise introduce significant latency.
