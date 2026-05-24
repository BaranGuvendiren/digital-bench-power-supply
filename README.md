# digital-bench-power-supply

## Disclaimer & Project Status
I started this project as a 2nd-year Electronics Engineering student to learn power electronics and PCB design in practice.  

While university courses mostly provided hypothetical ideal circuits, this project forced me to confront real-world effects on circuits (e.g., parasitic inductance, ESR, switching noise).

- **No Warranty:** This is **not** a consumer-grade product. While I tried to follow standard engineering practices, it has not undergone any formal testing (such as EMC).

***Current Status:*** *On-going*

***Documentation Notes***:  
- *Currently specified values (voltages, currents, frequencies) are initial design targets and may be optimized later based on future simulations and hardware testing.*
- *Detailed mathematical calculations, circuit schematics and simulation results are currently being formatted and will be documented in their respective sections soon.*

## Features
### Connections & Power
- Powered by a standard laptop adapter (19–20 V, ≥ 65 W) (2.5mm DC Barrel Jack).
- Includes a USB-C port and SWD pins for PC connection and debugging.
### Protection & Safety
- Reverse polarity protection via P-MOSFET, integrated with a mechanical switch on the gate for system ON/OFF control.
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

## Hardware Architecture & Design Steps
### Stage 1: Power Input & Input Filtering
* **Input Pre-Filtering:** For this design, it was assumed that standard laptop adapters operate around ~100 kHz switching frequency. To minimize this input noise, a CLC pi filter is placed immediately after the input.
  
* **Switching Frequency Planning:** To avoid intermodulation distortion caused by overlapping switching frequencies, the system frequencies are explicitly separated:
    - Laptop Adapter: ~100 kHz
    - Main Buck Regulator: 435 kHz
    - Auxiliary 5V Buck Regulator: 1 MHz
