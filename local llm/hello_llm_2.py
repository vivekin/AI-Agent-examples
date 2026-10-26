"""
Call a model from Python.

Prerequisite: Step 2 done (Ollama running with a model pulled).
Install:  pip install openai
Run:      python hello_llm_2.py

Later, to use a paid API instead, change only these three things:
  base_url, api_key, MODEL
"""
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")  # key ignored locally
MODEL = "qwen3.5:0.8b"  # must match a model you pulled (see `ollama list`)

# ---- 1. The simplest possible call ----------------------------------------
response = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "What is a token in an LLM? One sentence."}],
    reasoning_effort="none",
)
print(response.choices[0].message.content)

# ---- 2. Look at token usage (cost and context window are counted in tokens) -
print("\nprompt tokens:", response.usage.prompt_tokens)
print("answer tokens:", response.usage.completion_tokens)

# ---- 3. Add a system prompt and compare ------------------------------------
response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a pirate. Answer in max 2 sentences."},
        {"role": "user", "content": "What is a token in an LLM?"},
    ],
    reasoning_effort="none",
)
print("\nWith system prompt:\n", response.choices[0].message.content)

# ---- 4. Temperature: 0 = predictable, high = creative ----------------------
for temp in (0, 1.5):
    r = client.chat.completions.create(
        model=MODEL,
        temperature=temp,
        messages=[{"role": "user", "content": "Give me a name for a coffee shop. Just the name."}],
        reasoning_effort="none",
    )
    print(f"\ntemperature={temp}:", r.choices[0].message.content.strip())

# ---- 5. Streaming: tokens arrive one by one (this is autoregressive generation)
print("\nStreaming: ", end="")
stream = client.chat.completions.create(
    model=MODEL,
    stream=True,
    messages=[{"role": "user", "content": "Count from 1 to 10 in words."}],
    reasoning_effort="none",
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="", flush=True)
print()

# ---- 6. A tiny chatbot: the model has no memory, YOU resend the history -----
print("\nChat (type 'quit' to stop). Notice the model only 'remembers' what you resend.")
history = [{"role": "system", "content": "You are a helpful, concise assistant."}]
while True:
    user = input("you: ")
    if user.strip().lower() == "quit":
        break
    history.append({"role": "user", "content": user})
    r = client.chat.completions.create(model=MODEL, messages=history, reasoning_effort="none",)
    answer = r.choices[0].message.content
    history.append({"role": "assistant", "content": answer})
    print("bot:", answer)
    print(f"     (prompt tokens now: {r.usage.prompt_tokens}, grows every turn)")
