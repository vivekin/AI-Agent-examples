from llama_cpp import Llama

MODEL_PATH = "models/qwen2.5-0.5b-instruct-q4_k_m.gguf"

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    verbose=False,
)

response = llm.create_chat_completion(
    messages=[
        {"role": "user", "content": "Write a haiku about running AI on your own computer."}
    ],
    max_tokens=100,
    temperature=0.7,
)

print(response["choices"][0]["message"]["content"])