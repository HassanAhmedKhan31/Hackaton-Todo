# Feature: AI Chatbot (Phase III)

## Requirements
1. **Conversational Interface:**
   - Add a Chat Interface to the Frontend using OpenAI ChatKit.
2. **AI Agent (Backend):**
   - Implement an endpoint `POST /api/chat`.
   - Use **OpenAI Agents SDK** to process natural language.
   - The Agent must be **stateless** (store conversation history in the DB).
3. **MCP Server (Tools):**
   - The Agent cannot touch the DB directly. It must use **MCP Tools**.
   - Create Tools: `add_task`, `list_tasks`, `delete_task`, `complete_task`.
4. **Natural Language Understanding:**
   - The bot must understand: "Add a task to call Mom" -> Calls `add_task("Call Mom")`.