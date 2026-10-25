"""
Talk to a local model from Python and watch tokens, system prompts and few-shot.

Setup (once):
  1. Install Ollama from https://ollama.com
  2. ollama pull gemma3:4b        # or any small model you like (see `ollama list`)
  3. pip install openai
Ollama serves an OpenAI-compatible API on localhost:11434, so the same code
works later with a paid API: change base_url, api_key and MODEL.
"""
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")  # key is ignored locally
MODEL = "gemma3:4b"  # must match a model you pulled


def ask(messages, temperature=0.7):
    r = client.chat.completions.create(model=MODEL, messages=messages, temperature=temperature)
    print(r.choices[0].message.content.strip())
    u = r.usage
    print(f"  [tokens: prompt={u.prompt_tokens}, answer={u.completion_tokens}]\n")


question = "Explain what an embedding is."

print("--- 1. Zero-shot, no system prompt ---")
ask([{"role": "user", "content": question}])

print("--- 2. With a system prompt ---")
ask([
    {"role": "system", "content": "You are a patient teacher. Use one everyday analogy and max 3 sentences."},
    {"role": "user", "content": question},
])

print("--- 3. Few-shot: teach a format by example ---")
ask([
    {"role": "system", "content": "Answer in the exact format shown."},
    {"role": "user", "content": "Explain: token"},
    {"role": "assistant", "content": "Token | a small chunk of text | like a Lego brick of a sentence"},
    {"role": "user", "content": "Explain: context window"},
    {"role": "assistant", "content": "Context window | how much text the model sees at once | like a desk that can hold only so many pages"},
    {"role": "user", "content": "Explain: embedding"},
])

print("--- 4. Chain of thought ---")
ask([{"role": "user", "content": "A shop sells pens at 12 rupees. I buy 7 and pay with a 100 rupee note. "
                                  "What change do I get? Think step by step."}], temperature=0)

print("--- 5. Temperature: same prompt, run twice at high temperature ---")
for _ in range(2):
    ask([{"role": "user", "content": "Give me a name for a coffee shop."}], temperature=1.2)
