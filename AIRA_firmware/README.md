# AIRA Firmware

This repository contains the firmware and development tools for the **AIRA robot**.

⚠️ Primary development will be done using **MicroPython on the Raspberry Pi Pico W**.  
The C firmware is kept but is not the main workflow.

---

## 📁 Folder Structure

### `micropython/`
Main runtime firmware for the robot.

- `main.py` – Entry point (runs automatically on boot)
- `ble_advertising.py` – BLE helper utilities

This folder is the only one uploaded to the Pico when using MicroPico.
This can be done with **>MicroPico: Upload project to Pico**
You can use **>MicroPico: Delete all files from board** if there is any junk in the pi pico.

---

### `c_firmware/`
Pico SDK (C/C++) implementation of motor control.
Not currently used for development.

---

### `tools/`
Helper scripts that run on the computer (not on the Pico).

Examples:
- Serial testing scripts
- BLE upload helpers
- Debug utilities

These are development utilities only.

---

### `firmware/`
UF2 firmware files.

- `micropython-pico-w.uf2` – MicroPython firmware
- `pico-clean.uf2` – Reset/clean firmware

Used only when flashing the board in BOOTSEL mode.

---

## Primary Workflow (MicroPython)

1. Flash MicroPython UF2 to the Pico W (if not already installed).
2. Open the `micropython/` folder in VS Code.
3. Use the MicroPico extension.
4. Run:
   - `MicroPico: Delete all files from board`
   - `MicroPico: Upload project to Pico`
5. The robot will auto-run `main.py` on boot.

---

## 📘 Documentation

Complete documentation:

https://docs.google.com/document/d/1QjDEWNrOo2-5DQ1MAslLPjPbAI6OUzMq-Q01kJLjXpU/edit?usp=sharing

---

## Robot Overview

AIRA is a four motor drive robot powered by a Raspberry Pi Pico W. With plans to use a Jetson Aura Nano for higher level processing and sensor use. 
Control is currently done via:

- USB Serial commands
- Bluetooth Low Energy

---

## Future Development

Planned features:
- Sensor integration and fusion
- Autonomous navigation
- Communication with other robots

---
