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
- NPN-based active current sink at the output rail to maintain LDO stability under zero-load or light-load conditions.
### Output
- Digitally adjustable output (1.2–15 V, up to 2.75 A) with custom constant current (CC) mode.
- LDO output with buck controller as a pre-regulator.
- Multi-stage filtering.
- OLED display module.

*Note: A third-party display module is used to prevent the project scope from becoming excessively broad.*

## Design Goals
- Portable design.
- Low-noise output.

## Hardware Architecture Overview
This section provides a simplified blueprint of the system architecture, focusing on the core operating principles and critical design blocks without getting into mathematical formulas or component details.

### Stage 1: Power Input & Input Filtering
* **Input Pre-Filtering:** For this design, it was assumed that standard laptop adapters operate around ~100 kHz switching frequency. To minimize this input noise, a CLC Pi-filter is placed immediately after the input.
  
* **Switching Frequency Planning:** To prevent beat frequency interference and cross-rail noise coupling, the system frequencies are explicitly separated:
    - Laptop Adapter: ~100 kHz
    - Main Buck Regulator: 435 kHz
    - Auxiliary 5V Buck Regulator: 1 MHz

*Note: Other than common power input, both power rails ("Stage 2A" and "Stage 2B") are independent from each other.*

### Stage 2A: Main Adjustable Power Rail (Buck Converter & LDO)
* **Pre-Regulation:** To achieve stable and low-noise output, an LDO is used. However, since possible high output current may cause an impractical amount of power dissipation, a buck pre-regulator is implemented to maintain a minimal and constant dropout voltage.

* **CC & CV Modes:** While the Constant Current (CC) and Constant Voltage (CV) limits are digitally set by the MCU, relying solely on software poses a reliability risk in high-noise power environments. Therefore, a hardware resistor network restricts the maximum voltage the feedback circuit can receive, preventing the V-set signal from exceeding safe operational thresholds.
  
* **Current and Voltage Sensing:** The output current is measured using a shunt resistor paired with a current sense amplifier. The output voltage is sampled via a dedicated voltage divider connected to the LDO output rail. Both analog signals are then processed by the MCU's ADC and displayed on the OLED screen.

### Stage 2B: Auxiliary Power Rails (5 V Buck & 3.3 V LDOs)
* **Two-Level Regulation & Noise Isolation:** A 5 V Buck regulator serves as a pre-regulator for the 3.3 V LDOs, while directly powering the fan and the external display. To achieve clean signal processing, separate LDOs are dedicated to the analog and digital rails. This isolation prevents high-frequency digital switching noise from coupling into the sensitive analog rail. Additionally, both LDO lines include a ferrite bead Pi-filter at their inputs to block high-frequency EMI noise that LDOs struggle to suppress.

* **Temperature-Controlled PWM Fan:** To optimize thermal management and minimize both acoustic and electrical noise, the cooling fan operates only when required. The MCU monitors the system temperature and drives an N-MOSFET via PWM to dynamically adjust the fan speed proportional to the device temperature.
