# Design Calculations & Component Selection
This document contains the theoretical calculations and engineering decisions used to determine the component values for each stage of the power supply.

The datasheet files containing manufacturer specifications and references used in these calculations are located in the [`datasheets/`](/datasheets/) directory of this repository.

*Note: Some calculations are based on idealized formulas with sufficient design margin to ensure system stability and flexibility in component selection.*

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
| **2** | TPS54332 | Auxiliary Buck Pre-Regulator | 
| **3** | LP5907 | Auxiliary LDO | 

## Variable Tables
### Board Variables
| Variable | Description | MIN | TYP | MAX | UNIT | Source / Note |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| V<sub>IN</sub> | Input Voltage | 18.0 | 19.0 | 20.0 | V | Standard Laptop DC Power Adapter |
| V<sub>OUT</sub> | Adjustable Output Voltage | 1.25 | — | 15.0 | V | User/Load Dependent |
| f<sub>SW</sub> | Input Switching Frequency | 60 | 100 | 140 | kHz | Estimated Adapter Switching Frequency |
| P<sub>IN</sub> | Total Input Power | — | — | 51.47 | W | Combined Worst-Case Input Power |
| I<sub>IN</sub> | Input Current | — | — | 2.86 | A | Max Current Drawn from Adapter |
| I<sub>OUT</sub> | Output Load Current | — | — | 2.75 | A | Hardware Current Limit Boundary |
| C<sub>IN(EQ)</sub> | Equivalent Filter Capacitance | — | 120 | — | μF | Calculated Equivalent Input Capacitance |
| L<sub>IN</sub> | Input Filter Inductance | — | 6.8 | — | μH | Selected Power Inductor |

### IC-1 LM25117 Variables
| Variable | Description | MIN | TYP | MAX | UNIT | Source / Note |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| η<sub>(1)</sub> | Output Efficiency | 85 | 90 | 95 | % | Estimated Efficiency Range |
| f<sub>SW(1)</sub> | Switching Frequency | — | 435 | — | kHz | Set Switching Frequency |

### IC-2 TPS54332 Variables
| Variable | Description | MIN | TYP | MAX | UNIT | Source / Note |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| V<sub>OUT(2)</sub> | Output Voltage | — | 5.0 | — | V | Supplied by V<sub>IN</sub> |
| I<sub>OUT(2)</sub> | Output Current | — | 0.5 | — | A | Estimated Max Load |
| η<sub>(2)</sub> | Output Efficiency | 85 | 90 | 95 | % | Estimated Efficiency Range |
| f<sub>SW(2)</sub> | Switching Frequency | — | 1 | — | MHz | Fixed Switching Frequency |

### IC-3 LP5907 Variables
| Variable | Description | MIN | TYP | MAX | UNIT | Source / Note |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| V<sub>IN(3)</sub> | Input Voltage | — | 5.0 | — | V | Equal to V<sub>OUT(2)</sub> |
| V<sub>OUT(3)</sub> | Output Voltage | — | 3.3 | — | V | Separate Rails for Analog and Digital |

## Math Calculations
### Stage 1: Power Input & Input Filter
#### Middlebrook Criteria Confirmation
To meet the Middlebrook criteria, input impedance of the load must be at least 10x greater than output impedance of the source. To account for worst case scenario, at lowest input impedance, minimum value of input voltage ($\rm V_{IN}$) is used.

$$
\begin{aligned}
\rm P_{IN(1)} & = \rm \frac{ I_{OUT} \cdot V_{OUT}}{\upeta_{(1)}}\ [W] \\
  & = \frac{2.75 \cdot 15.0}{0.85} \\
  \newline
  & \approx \rm 48.53\ W
\end{aligned}
\qquad\qquad
\begin{aligned}
\rm P_{IN(2)} & = \rm \frac{ I_{OUT(2)} \cdot V_{OUT(2)}}{\upeta_{(2)}}\ [W] \\
  & = \frac{0.5 \cdot 5.0}{0.85} \\
  \newline
  & \approx \rm 2.94\ W
\end{aligned}
$$

$$
\begin{aligned}
\rm P_{IN} & = \rm P_{IN(1)} + P_{IN(2)}\ [W] \\
  & = 48.53 + 2.94 \\
  \newline
  & = \rm 51.47\ W \\
\newline
\newline
\rm Z_{IN} & = \rm \frac{V_{IN}^2}{P_{IN}}\ [\Omega] \\
  & = \frac{18^2}{51.47} \\
  \newline
  & \approx \rm 6.29\ \Omega
\end{aligned}
$$

For $\rm Z_{IN} \geq 10 \cdot Z_{OUT(FILTER)}$ to be true, output impedance of the source ($\rm Z_{OUT(FILTER)}$) must be less than $0.67\ \rm \Omega$. ($\rm L_{IN}$ is selected as standard value of 6.8 $\rm \upmu H$.)

$$
\begin{aligned}
\rm Z_{OUT(FILTER)} & = \rm \sqrt{\frac{L_{IN}}{C_{IN(EQ)}}}\ [\Omega] \\
  & = \sqrt{\frac{6.8 \cdot 10^{-6}}{120 \cdot 10^{-6}}} \\
  \newline
  & \approx \rm 0.24\ \Omega\ \(\text{26x less than}\ Z_{IN}\)
\end{aligned}
$$

#### Cut-off Frequency Confirmation
To reduce noise coupling at the input node, the cutoff frequency of the low-pass filter should be at least 10x lower than the switching frequency. 

For a conservative baseline, the nominal adapter switching frequency ($\rm f_{SW} \approx \rm 100 kHz$) is considered. Although adapters typically have relatively low output ripple, designing with a sufficiently low cut-off frequency increases attenuation of input ripple and suppress noise coupling between the other switching regulators connected to that node.

$$
\begin{aligned}
\rm f_{C} &= \rm \frac{1}{2 \uppi \sqrt{L_{IN} \cdot C_{IN(EQ)}}} \\
  & = \frac{1}{2 \uppi \sqrt{(6.8 \cdot 10^{-6}) \cdot (120 \cdot 10^{-6})}} \\
  \newline
  & \approx \rm 5.57\ kHz\ \(\text{17x less than}\ f_{SW}\)
\end{aligned}
$$

#### Input MOSFET Heat Dissipation [TBD]

*Note: Some of the components are To Be Determined [TBD] based on availability and final layout space constraints.*
