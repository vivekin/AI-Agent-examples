# Quickstart: run a language model on an ESP32-S3

The model is flashed into the chip, not installed. You build the firmware on your computer and push it over USB. This uses doryiii's esp32-llm project, which already includes TinyStories models.

Hardware: an ESP32-S3 with 8 MB PSRAM (e.g. Waveshare ESP32-S3 boards, or any N8R8 / N16R8 dev board), a USB-C cable, a Mac or Linux computer.

## 1. Install ESP-IDF (the build framework), about 20 min

```bash
brew install cmake ninja dfu-util python3        # macOS; on Linux use apt
mkdir -p ~/esp && cd ~/esp
git clone -b v5.3 --recursive https://github.com/espressif/esp-idf.git
cd esp-idf && ./install.sh esp32s3
```

Every new terminal, load the tools first:

```bash
. ~/esp/esp-idf/export.sh
```

## 2. Get the project (includes the models)

```bash
cd ~/esp
git clone https://github.com/doryiii/esp32-llm.git
cd esp32-llm
idf.py set-target esp32s3
```

## 3. Flash it

Plug the board in over USB-C, find the port, then build and flash:

```bash
ls /dev/cu.usbmodem*        # note the port name
idf.py -p /dev/cu.usbmodemXXX build flash monitor
```

First build takes a few minutes. When it finishes, the serial monitor shows a story streaming with a tokens-per-second number.

If flashing fails with "no serial data received": hold the BOOT button, tap RESET, release BOOT, then run the command again.

## 4. Switch models (optional)

The repo ships two models. To use the larger 3.3M INT8 one:

```bash
idf.py menuconfig
```

Find the LLM configuration section, select the INT8 / 3M model, save, exit, then reflash with the same build command.

## Notes

- The model lives in flash forever. Unplug the board, power it from any USB charger, and it keeps generating on its own.
- Ceiling on this chip is about 3.3M parameters. These are "toy" models that write simple children's stories, which is the point.
- Ctrl+] exits the serial monitor.
