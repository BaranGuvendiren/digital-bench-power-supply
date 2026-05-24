# digital-bench-power-supply

## Disclaimer & Project Status
I started this project as a 2nd-year Electronics Engineering student to learn power electronics and PCB design in practice.  

While university courses mostly provided hypothetical ideal circuits, this project forced me to confront real-world effects on circuits (e.g., parasitic inductance, ESR, switching noise).

- **No Warranty:** This is **not** a consumer-grade product. While I tried to follow standard engineering practices, it has not undergone any formal testing (such as EMC).

***Current Status:*** *On-going*

## Features
### Connections & Power
- Powered by a standard laptop adapter (19–20 V, ≥ 65 W) (2.5mm DC Barrel Jack).
- Includes a USB-C port and SWD pins for PC connection and debugging.
### Protection & Safety
- Reverse polarity protection with P-MOSFET.
- Temperature-controlled fan.
### Output
- Digitally adjustable output (1.2–15 V, up to 2.75 A) with custom constant current (CC) mode.
- LDO output with buck controller as a pre-regulator.
- Multi-stage filtering.
- OLED display module.

*Note: A third-party display module is used to prevent the project scope from becoming excessively broad.*

## Design Goals
- Portable design.
- Low-noise output.
