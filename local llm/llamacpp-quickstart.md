# Quickstart: download a model and serve it with llama.cpp

Use this when you want an OpenAI-compatible API on your own machine, when you need a specific quantization Ollama does not offer, or when serving very large models. Works on Mac, Linux, and the AMD/PC boxes.

## 1. Install llama.cpp

Mac:
```bash
brew install llama.cpp
```

Or build from source (needed for AMD Vulkan, Nvidia CUDA, etc.):
```bash
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
cmake -B build                       # add -DGGML_CUDA=ON for Nvidia, -DGGML_VULKAN=ON for AMD
cmake --build build --config Release -j
```

## 2. Download a model (GGUF format)

llama.cpp does not have a model store. Pull the GGUF file from Hugging Face:

```bash
pip install -U "huggingface_hub[cli]"
mkdir -p ~/models && cd ~/models
hf download unsloth/Qwen3-32B-GGUF --include "*Q4_K_M*" --local-dir qwen3-32b
```

Check the model's Hugging Face page for the exact filename pattern. `Q4_K_M` is the standard quality/size tradeoff. Lower numbers (Q3, Q2) are smaller and worse.

## 3. Serve it

```bash
llama-server -m ~/models/qwen3-32b/*.gguf --host 0.0.0.0 --port 8080 -ngl 99 -c 8192
```

- `--host 0.0.0.0` lets other devices on your network reach it (leave it off for local-only)
- `-ngl 99` puts all layers on the GPU
- `-c 8192` is the context length

## 4. Call it

Same shape as the OpenAI API:

```bash
curl http://localhost:8080/v1/chat/completions -d '{
  "messages":[{"role":"user","content":"Say hi in five words."}],
  "max_tokens":30
}'
```

Any tool that speaks the OpenAI API (your own scripts, an agent framework, even a microcontroller over Wi-Fi) can now point at this URL.

## 5. Measure speed (optional)

```bash
llama-bench -m ~/models/qwen3-32b/*.gguf -ngl 99
```

Prints prompt-processing and generation tokens-per-second.

## Notes

- Model size at Q4 is roughly params × 0.6 GB. A 32B is ~18 GB, a 70B ~40 GB.
- Big MoE or high-context models often ship as several split GGUF files; download the whole set and point `-m` at the first one.
- To keep it running across reboots, wrap the `llama-server` command in a launchd job (Mac) or systemd service (Linux).
