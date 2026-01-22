import os
import json
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from backend.mcp.server import TodoMCP

# Automatically find and load the .env file
load_dotenv(find_dotenv())

class TodoAgent:
    def __init__(self):
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("❌ ERROR: OPENROUTER_API_KEY not found in environment!")
        else:
            print("✅ OPENROUTER_API_KEY found.")

        # OpenRouter Integration
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            default_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "Hackathon Todo",
            }
        )
        self.mcp = TodoMCP()
        self.tools = self.mcp.get_tools()

    def run(self, user_message: str) -> str:
        # Improved system prompt to force tool usage
        messages = [
            {
                "role": "system", 
                "content": "You are a specialized Todo Assistant. When a user asks to 'add', 'buy', or 'create' something, you MUST use the provided tools to update the database. Always confirm the action was successful based on the tool output."
            },
            {"role": "user", "content": user_message}
        ]

        while True:
            # MiMo-V2-Flash reasoning requirement
            response = self.client.chat.completions.create(
                model="xiaomi/mimo-v2-flash:free",
                messages=messages,
                tools=self.tools,
                tool_choice="auto",
                extra_body={"reasoning": {"enabled": True}}
            )

            response_message = response.choices[0].message
            
            # Prepare the assistant message for history
            assistant_msg = {
                "role": "assistant",
                "content": response_message.content or "",
            }
            
            if hasattr(response_message, 'reasoning_details'):
                assistant_msg["reasoning_details"] = response_message.reasoning_details
            
            if response_message.tool_calls:
                assistant_msg["tool_calls"] = [
                    tool_call.model_dump() for tool_call in response_message.tool_calls
                ]

            messages.append(assistant_msg)

            tool_calls = response_message.tool_calls
            if tool_calls:
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    try:
                        # This executes the actual database logic
                        tool_result = self.mcp.call_tool(function_name, function_args)
                        
                        if hasattr(tool_result, 'model_dump'):
                            tool_result = tool_result.model_dump()
                        elif isinstance(tool_result, list):
                            tool_result = [
                                item.model_dump() if hasattr(item, 'model_dump') else item 
                                for item in tool_result
                            ]
                        
                        content = json.dumps(tool_result) if not isinstance(tool_result, str) else tool_result
                    except Exception as e:
                        content = f"Error: {str(e)}"

                    # Feed the result back to the AI so it knows the task was added
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": content,
                    })
                # Loop continues so the model can read the 'success' message and reply to user
            else:
                # No more tools to call, return the final text
                return response_message.content if response_message.content else "Task processed successfully."

# Initialize agent
agent = TodoAgent()
 