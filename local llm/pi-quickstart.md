# Quickstart: run a model on a Raspberry Pi 5

The Pi runs a full operating system, so you install models the easy way, with Ollama.

Hardware: Raspberry Pi 5 (8 GB recommended), the official 27W power supply, a microSD card, and another computer to SSH from. Optional: a USB mic and speaker for voice.

## 1. Flash the OS

On your main computer, install Raspberry Pi Imager (raspberrypi.com/software). Insert the microSD, then in Imager:

- Device: Raspberry Pi 5
- OS: Raspberry Pi OS (64-bit)
- Storage: the card
- Click Edit Settings and set: a hostname (e.g. `mypi`), a username and password, your Wi-Fi name and password, and enable SSH.

Write, then put the card in the Pi and power it on. Wait about 90 seconds.

## 2. Connect

From your main computer, on the same Wi-Fi:

```bash
ssh yourname@mypi.local
```

## 3. Install Ollama and run a model

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama run qwen3:1.7b
```

That downloads the model and drops you into a chat. Type a question, get an answer. Type `/bye` to exit. Add `--verbose` to see the tokens-per-second.

Good starting models for an 8 GB Pi:
- `qwen3:0.6b` — fast
- `qwen3:1.7b` — the daily driver
- `qwen3:8b` — runs but slow (about 2 tok/s), good for showing the ceiling
- `moondream` — describes images

## 4. Chain models (optional, the fun part)

Because it has an OS, the Pi can run several models together. A voice assistant is Whisper (hears) plus an LLM (thinks) plus Piper (speaks), each installed with pip in a Python virtual environment. That is a longer build, but the single-model chat above works in five minutes.

## Notes

- Shut down cleanly before pulling power: `sudo shutdown -h now`. Yanking power can corrupt the card.
- The first run of any model loads it from the card and is slower; the second run is the real speed.
