# Design Calculations & Component Selection
This document contains the theoretical calculations and engineering decisions used to determine the component values for each stage of the power supply.

The datasheet files containing manufacturer specifications and references used in these calculations are located in the [`datasheets/`](/datasheets/) directory of this repository.

## Naming Conventions & Notation
To maintain mathematical clarity across multiple stages, variables are named using the following conventions:

| Notation Format | Description | Example |
| :--- | :--- | :--- |
| **No Parentheses** | Global board-level variable | $\rm V_{OUT}$ (Board output voltage) |
| **With Parentheses** | Component specific to a certain IC | $\rm V_{OUT(1)}$ (Output voltage specific to IC1 - LM25117) |

*Note: The number inside the parentheses indicates which integrated circuit (IC) the variable belongs to.*

## IC Reference Table
| IC Number | Component Name | Description |
| :---: | :--- | :--- |
| **1** | LM25117 | Main Buck Pre-Regulator |

## Variable Tables
### Board Variables
| Variable | Description | MIN | TYP | MAX | UNIT | Source / Note |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| V<sub>IN</sub> | Input Adapter Voltage | 18.0 | 19.0 | 20.0 | V | Standard Laptop DC Power Adapter |
| V<sub>OUT</sub> | Adjustable Output Voltage | 1.25 | — | 15.0 | V | User/Load Dependent |
| f<sub>SW</sub> | Input Switching Frequency | 60 | 100 | 140 | kHz | Estimated |
| I<sub>OUT</sub> | Output Load Current | — | — | 2.75 | A | Hardware Current Limit Boundary |
