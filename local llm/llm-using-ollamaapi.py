
import ollama

response = ollama.chat(
    model="qwen3.5:0.8b",
    messages=[
        {
            "role": "user",
            "content": "Why would someone run an AI model locally? One sentence."
        }
    ],
    think=False,
)

print(response["message"]["content"])
