from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

response = client.chat.completions.create(
    model="qwen3.5:0.8b",  # any model you've pulled with `ollama pull`
    messages=[
        {"role": "system", "content": "You are a 2 year old baby."},
        {
            "role": "user",
            "content": "Why would someone run an AI model locally? One sentence.",
        }
    ],
    reasoning_effort="none",
)

print(response.choices[0].message.content)
print("===========================================")

response = client.chat.completions.create(
    model="qwen3.5:0.8b",  # any model you've pulled with `ollama pull`
    messages=[
        {"role": "system", "content": "You are a local AI assistant."},
        {
            "role": "user",
            "content": "Explain quantum computing in one sentence.",
        },
    ],
    reasoning_effort="none",
)

print(response.choices[0].message.content)