# Quickstart: connect an Arduino Uno R4 WiFi to a model on another machine

The R4 has 32 KB of RAM, far too little to run any model. Instead it acts as a thin client: it sends a question over Wi-Fi to a machine that IS running a model (a Mac Studio, a laptop, a Pi, an AMD box, anything with an OpenAI-compatible server), and shows the reply on its built-in LED matrix.

Hardware: Arduino Uno R4 WiFi, a USB-C cable, a computer to flash from, and a machine on the same Wi-Fi already serving a model.

## 1. Make the model reachable on the network

The serving machine must listen on all network interfaces, not just localhost, and you need its LAN IP.

If it runs llama.cpp:
```bash
llama-server -m <model.gguf> --host 0.0.0.0 --port 8080 -ngl 99
```

If it runs Ollama:
```bash
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

Get the machine's IP (on a Mac): `ipconfig getifaddr en0`. Note it, e.g. `192.168.1.50`.

Test from another computer on the same Wi-Fi before touching the Arduino:
```bash
# llama.cpp
curl http://192.168.1.50:8080/v1/chat/completions -d '{"messages":[{"role":"user","content":"Say hi."}],"max_tokens":20}'
# Ollama
curl http://192.168.1.50:11434/api/generate -d '{"model":"qwen3:1.7b","prompt":"Say hi.","stream":false}'
```
This must return text before you continue. If it fails to connect, the server is still localhost-only; fix the host flag above.

## 2. Set up the Arduino IDE

1. Arduino IDE, Boards Manager, install "Arduino UNO R4 Boards".
2. Library Manager, install "ArduinoGraphics" (for the scrolling text).
3. Plug in the R4, select Board: Arduino UNO R4 WiFi, and the right Port.
4. Upload the stock Blink example to confirm the board works. If the IDE offers a Wi-Fi firmware update, accept it.

## 3. The sketch

Fill in the four values at the top: your Wi-Fi, the server IP, and match the two server-specific lines to llama.cpp OR Ollama.

```cpp
#include "WiFiS3.h"
#include "ArduinoGraphics.h"
#include "Arduino_LED_Matrix.h"

#define WIFI_SSID   "your-wifi"
#define WIFI_PASS   "your-password"
#define SERVER_IP   "192.168.1.50"
#define SERVER_PORT 8080                       // 11434 for Ollama

// llama.cpp: path /v1/chat/completions, reply field "content"
// Ollama:    path /api/generate,        reply field "response"
const char* SERVER_PATH = "/v1/chat/completions";
const char* MARKER      = "\"content\":\"";
const char* PROMPT      = "Say one short cheerful sentence.";

ArduinoLEDMatrix matrix;
WiFiClient client;
static char reply[160];

void setup() {
  Serial.begin(115200);
  matrix.begin();
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) delay(500);
  Serial.print("IP: "); Serial.println(WiFi.localIP());
}

void loop() {
  if (ask()) { Serial.println(reply); scroll(reply); }
  else scroll("error");
  delay(20000);
}

bool ask() {
  if (!client.connect(SERVER_IP, SERVER_PORT)) return false;
  // llama.cpp body. For Ollama use:
  //   {"model":"qwen3:1.7b","prompt":"...","stream":false}
  String body = "{\"messages\":[{\"role\":\"user\",\"content\":\"";
  body += PROMPT;
  body += "\"}],\"max_tokens\":40}";

  client.print("POST "); client.print(SERVER_PATH); client.print(" HTTP/1.1\r\nHost: ");
  client.print(SERVER_IP);
  client.print("\r\nContent-Type: application/json\r\nConnection: close\r\nContent-Length: ");
  client.print(body.length()); client.print("\r\n\r\n"); client.print(body);

  int mlen = strlen(MARKER), matched = 0, n = 0; bool in = false;
  unsigned long t0 = millis();
  while (client.connected() || client.available()) {
    if (millis() - t0 > 30000) break;
    if (!client.available()) { delay(1); continue; }
    char c = client.read();
    if (!in) { matched = (c==MARKER[matched]) ? matched+1 : (c==MARKER[0]?1:0);
               if (matched==mlen) in = true; }
    else { if (c=='\\'){ char e=client.read(); c=(e=='n')?' ':e; }
           else if (c=='"') break;
           if (n < (int)sizeof(reply)-1) reply[n++] = c; }
  }
  reply[n] = 0; client.stop(); return n > 0;
}

void scroll(const char* t) {
  matrix.beginDraw(); matrix.stroke(0xFFFFFFFF);
  matrix.textScrollSpeed(60); matrix.textFont(Font_5x7);
  matrix.beginText(0, 1, 0xFFFFFF); matrix.println(t);
  matrix.endText(SCROLL_LEFT); matrix.endDraw();
}
```

Upload, open Serial Monitor at 115200. You should see an IP line, then a sentence every 20 seconds, scrolling across the LED matrix at the same time.

## 4. The cordless shot

Unplug from the computer and power the R4 from any USB charger or power bank. It rejoins Wi-Fi and keeps asking the model on its own. A 32 KB chip answering with a model running on a much bigger machine.

## Switching to a different brain

Change two lines and reflash to point at any other machine:

| Serving machine | SERVER_IP / PORT | SERVER_PATH | MARKER |
|---|---|---|---|
| Mac Studio / AMD (llama.cpp) | its IP / 8080 | /v1/chat/completions | "content":" |
| Laptop / Pi (Ollama) | its IP / 11434 | /api/generate | "response":" |

For Ollama also change the request body to the `{"model":...,"prompt":...,"stream":false}` form noted in the sketch.

## Troubleshooting

- Never joins Wi-Fi: the R4 is 2.4 GHz only. If your router splits bands, use the 2.4 GHz network name.
- Joins but every request fails: run the curl from step 1 from another computer. If that works but the R4 does not, the router may isolate wireless clients (look for "AP isolation" and turn it off).
- Reply is a wall of reasoning text: the model is "thinking". For Ollama add `,"think":false` to the body; for llama.cpp add `,"chat_template_kwargs":{"enable_thinking":false}`.
