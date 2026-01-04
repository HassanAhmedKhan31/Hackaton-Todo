# AGENTS.md

# Purpose
This project uses **Spec-Driven Development (SDD)**. No agent is allowed to write code until the specification is complete.

# Workflow (Source of Truth)
1. **Constitution** (`specs/constitution.md`): Principles & Constraints.
2. **Specify** (`specs/features/*.md`): Requirements & User Stories.
3. **Plan** (`specs/architecture.md`): Component breakdown & Logic.
4. **Tasks** (`specs/tasks.md`): Atomic, testable work units.
5. **Implement**: Code only what the current Task authorizes.

# Agent Rules
1. **Never generate code without a referenced Task ID.**
2. If a spec is missing, stop and request it.
3. Every code file must reference the Task ID in comments.
4. **Tech Stack Constraints:**
    - **Frontend:** Next.js (App Router), Tailwind CSS.
    - **Backend:** FastAPI, SQLModel.
    - **Infrastructure:** Docker, Kubernetes (Minikube).