# Hackathon Project: AI-Powered Todo App

This document provides a technical overview of the AI-Powered Todo App, built with Next.js, FastAPI, and Kubernetes.

## Technical Features

### Background AI Processing
- **Challenge:** Initial AI-powered task processing took up to 3 minutes, leading to a poor user experience with long loading times.
- **Solution:** We implemented `FastAPI BackgroundTasks` to offload the AI processing to a background job.
- **Result:** This reduced the perceived latency for the user from 3 minutes to less than 1 second. The UI is immediately updated, while the AI processing happens asynchronously.

### Automated Schema Fixes
- **Challenge:** During development, frequent changes to the data models required manual updates to the PostgreSQL database schema, which was error-prone and time-consuming.
- **Solution:** We created a `fix_schema.py` script that automatically detects and applies necessary schema migrations on application startup.
- **Result:** The database schema is always in sync with the application code, eliminating a whole class of potential runtime errors and streamlining development.

### Live UI Syncing
- **Challenge:** We needed a way to keep the UI in sync with the backend without requiring the user to manually refresh the page.
- **Solution:** We implemented a 5-second polling mechanism in the Next.js frontend. The UI calls a callback function to fetch the latest data from the backend every 5 seconds.
- **Result:** The UI is always up-to-date, providing a seamless and "live" user experience.

## Quick Start

To run this project locally, you will need `kubectl` access to a Kubernetes cluster.

1.  **Port-forward the backend service:**
    ```bash
    kubectl port-forward <backend-pod-name> 8000:8000
    ```
    This will make the backend API accessible at `http://localhost:8000`.

2.  **Port-forward the frontend service:**
    ```bash
    kubectl port-forward <frontend-pod-name> 3000:3000
    ```
    This will make the frontend UI accessible at `http://localhost:3000`.

## Project Reflection

As a graphic designer, this hackathon was a journey of growth. I started with a passion for user experience and a vision for an intuitive interface. However, bringing this vision to life required me to step out of my comfort zone and dive into the world of backend development, Kubernetes, and AI agents.

Learning to orchestrate a multi-service application with Kubernetes was a steep learning curve, but it was also incredibly rewarding. The ability to automate deployments and manage complex systems at scale is a powerful skill that I am excited to continue developing.

Working with AI agents was another highlight of this project. It was fascinating to see how we could leverage AI to create a more intelligent and helpful user experience.

This hackathon has been an incredible learning experience. It has not only expanded my technical skills but also given me a deeper appreciation for the collaboration between design and engineering. I am proud of the application we have built and excited to apply these new skills to future projects.
