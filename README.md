# Mouse Keyboard Pyramids (MKP)

Hybrid mouse + keyboard using pyramid-shaped touch/tilt keys. MKP combines capacitive touch, tilt sensing, and small-form HID firmware to provide an alternative input device for typing and pointing.

## Features
- Pyramid-shaped keys: touch shows cursor location; tilt selects symbols/directions.
- Position sensing: MPR121 capacitive touch controller (per-pyramid address).
- Tilt sensing: magnet-mounted mesh + Hall sensors detect X/Y tilt.
- Keyboard: 5×3 matrix (with diodes) + two dedicated joystick inputs.
- Pointing: optional optical sensor (PMW3360) and two side scroll wheels (one per side).
- Modular hardware: removable side modules with 4×AA battery holders and PCBs; LED backlight PCB under keyboard.
- Assembly designed for minimal tools; partly tool-free disassembly.
- Wireless option: Raspberry Pi Pico (or Pico W for Wi‑Fi); CircuitPython with Adafruit libraries and HID support.

## Software & Files
- CircuitPython code and example text editor included in repo root (Python).
- FreeCAD (part/assembly) models and KiCad schematics/PCB in respective folders.
- Datasheet folder contains BOM, diagrams, and images.

## License
CC‑BY‑4.0

## Contact
Serge Sokolov — sergesclv@gmail.com / sergesclv3@protonmail.com
