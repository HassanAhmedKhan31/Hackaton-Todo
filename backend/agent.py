import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from backend.mcp.server import TodoMCP

load_dotenv()

class TodoAgent:
    def __init__(self):
        # OpenRouter Integration
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            default_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "Hackathon Todo",
            }
        )
        self.mcp = TodoMCP()
        self.tools = self.mcp.get_tools()

    def run(self, user_message: str) -> str:
        """
        Runs the agent loop with improved error handling and cleaning.
        """
        messages = [
            {"role": "system", "content": "You are a helpful Todo Assistant. You have access to tools to manage tasks. Always verify the action was successful. Do NOT output raw XML tags like <tool_call> in your final response."},
            {"role": "user", "content": user_message}
        ]

        while True:
            response = self.client.chat.completions.create(
                model="xiaomi/mimo-v2-flash:free",
                messages=messages,
                tools=self.tools,
                tool_choice="auto",
            )

            response_message = response.choices[0].message
            messages.append(response_message)

            tool_calls = response_message.tool_calls
            if tool_calls:
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    try:
                        tool_result = self.mcp.call_tool(function_name, function_args)
                        
                        # Serialize result safely
                        if isinstance(tool_result, list):
                            content = json.dumps([t.model_dump() for t in tool_result])
                        elif hasattr(tool_result, "model_dump"):
                            content = json.dumps(tool_result.model_dump())
                        else:
                            content = str(tool_result)

                    except Exception as e:
                        content = f"Error calling tool: {str(e)}"

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": content,
                    })
            else:
                # --- CLEANING STEP ---
                final_text = response_message.content
                
                # If the AI tried to use a tool but failed to structure it, or left artifacts:
                if final_text and "<tool_call>" in final_text:
                    final_text = final_text.replace("<tool_call>", "").replace("</tool_call>", "")
                
                return final_text

# --- THIS LINE WAS MISSING ---
agent = TodoAgent()