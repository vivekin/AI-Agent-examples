
import ollama
from tools import get_cat_facts, get_current_time, get_weather

MODEL = "qwen3.5:0.8b"

# -----------------------------
# REGISTER AVAILABLE TOOLS
# -----------------------------

available_tools = {
    "get_weather": get_weather,
    "get_current_time": get_current_time,
    "get_cat_facts": get_cat_facts,
}


# -----------------------------
# AGENT LOOP
# -----------------------------

def run_agent():

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. "
                "Use available tools whenever necessary. "
                "After receiving tool results, explain them "
                "to the user."
            )
        }
    ]

    print("Ollama Tool Calling Assistant")
    print("Type 'exit' to quit.\n")

    while True:

        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        messages.append({
            "role": "user",
            "content": user_input
        })

        # Let the LLM decide whether to call a tool
        for _ in range(5):

            response = ollama.chat(
                model=MODEL,
                messages=messages,
                tools=list(available_tools.values()),
                think=False
            )

            assistant_message = response.message

            # Preserve assistant response in conversation history
            messages.append(assistant_message)

            # Check whether LLM requested any tools
            tool_calls = assistant_message.tool_calls or []

            if not tool_calls:
                print("\nAssistant:", assistant_message.content)
                break

            # Execute requested tools
            for tool_call in tool_calls:

                tool_name = tool_call.function.name
                arguments = tool_call.function.arguments

                print(f"\n[Tool requested: {tool_name}]")
                print("[Arguments]", arguments)

                # Find the actual Python function
                function = available_tools.get(tool_name)

                if function is None:
                    result = "Error: Unknown tool"
                else:
                    try:
                        result = function(**arguments)
                    except Exception as e:
                        result = f"Tool execution error: {e}"

                print("[Tool result]", result)

                # Send tool output back to the LLM
                messages.append({
                    "role": "tool",
                    "tool_name": tool_name,
                    "content": str(result)
                })

        else:
            print("Maximum tool-call iterations reached.")

        print()


if __name__ == "__main__":
    run_agent()
