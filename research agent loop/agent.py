"""
Research assistant: LLM + web search in a loop until done.
"""

import json
import os

import httpx
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DIVIDER = "-" * 50


def log(label: str, text: str = "") -> None:
    """Print a labeled step for demo / video recording."""
    if text:
        print(f"\n[{label}] {text}")
    else:
        print(f"\n[{label}]")


SYSTEM_PROMPT = """You are a research assistant. Search the web when you need current info.
Cite sources as markdown links. Never invent URLs.

Format:
## Summary
## Key findings (max 5 bullets with links)
## Sources
"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current information.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    }
]


def web_search(query: str) -> str:
    """Search the web with Firecrawl and return plain text for the model."""
    log("TOOL", f"web_search(query={query!r})")

    response = httpx.post(
        "https://api.firecrawl.dev/v2/search",
        headers={"Authorization": f"Bearer {os.environ['FIRECRAWL_API_KEY']}"},
        json={"query": query, "limit": 5},
        timeout=30,
    )
    response.raise_for_status()

    results = response.json().get("data", {}).get("web", [])
    if not results:
        log("TOOL", "returned 0 results")
        return "No results found."

    log("TOOL", f"returned {len(results)} results")

    lines = []
    for item in results:
        title = item.get("title", "Untitled")
        url = item.get("url", "")
        snippet = item.get("description", "")
        lines.append(f"- {title} ({url}): {snippet}")

    return "\n".join(lines)


def run_agent(client: OpenAI, messages: list, model: str) -> str:
    log("START", "Agent loop running (think -> act -> observe)")

    for turn in range(1, 6):
        print(DIVIDER)
        log("THINK", f"Turn {turn} - sending context to {model}")

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,
        )
        message = response.choices[0].message
        messages.append(message.model_dump(exclude_none=True))
        
        if message.content:
            log("MODEL", message.content)

        if not message.tool_calls:
            log("DONE", "Model finished - no more tools needed")
            return message.content or ""
        
        for call in message.tool_calls:
            args = json.loads(call.function.arguments)
            log("ACT", f"Model requested tool: {call.function.name}")
            log("ACT", f"Arguments: {json.dumps(args)}")
        
            result = web_search(args["query"])
            log("OBSERVE", "Tool result (fed back to model):")
            print(result)
        
            messages.append(
                {"role": "tool", "tool_call_id": call.id, "content": result}
            )
    
    log("STOP", "Hit max turns (5) without a final answer")
    return "Too many search rounds. Try a simpler question."


def main() -> None:
    client = OpenAI()
    model = os.getenv("OPENAI_MODEL", "gpt-4o")
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("Research Assistant (type quit to exit)\n")

    while True:
        question = input("You: ").strip()
        if question.lower() in {"quit", "exit", "q"}:
            break
        if not question:
            continue

        messages.append({"role": "user", "content": question})
        log("USER", question)

        answer = run_agent(client, messages, model)
        messages.append({"role": "assistant", "content": answer})

        print(DIVIDER)
        log("ANSWER", "Final response to user:")
        print(f"\n{answer}\n")


if __name__ == "__main__":
    main()