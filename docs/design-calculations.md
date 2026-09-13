# Design Calculations & Component Selection
This document contains the theoretical calculations and engineering decisions used to determine the component values for each stage of the power supply.

The datasheet files containing manufacturer specifications and references used in these calculations are located in the [`datasheets/`](/datasheets/) directory of this repository.

*Note: Some calculations are based on idealized formulas with sufficient design margin to ensure system stability and flexibility in component selection.*

## Naming Conventions & Notation
To maintain mathematical clarity across multiple stages, variables are named using the following conventions:

| Notation Format | Description | Example |
| :--- | :--- | :--- |
| **No Parentheses** | Global board-level variable | $\rm V_{OUT}$ (Board output voltage) |
| **With Parentheses** | Component specific to a certain IC | $\rm V_{OUT(1)}$ (Output voltage specific to U1 - LM25117) |

*Note: The number inside the parentheses indicates which integrated circuit (IC) the variable belongs to.*

## IC Reference Table
| IC Number | Component Name | Description |
| :---: | :--- | :--- |
| **1** | LM25117 | Main Buck Pre-Regulator |
| **2** | MIC29302 | Main LDO |
| **4** | TPS54331 | Auxiliary 5 V Buck Regulator | 
| **6** | TPS54332 | Auxiliary 12 V Buck Regulator | 

## Variable Tables
### Board Variables
| Variable | Description | MIN | TYP | MAX | UNIT | Source / Note |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| V<sub>IN</sub> | Input Voltage | 18.4 | 19.0 | 20.4 | V | Standard 19 V/20 V Laptop DC Power Adapter |
| V<sub>OUT</sub> | Adjustable Output Voltage | 1.25 | — | 13.8 | V | User/Load Dependent |
| f<sub>SW</sub> | Adapter Switching Frequency | 60 | 100 | 140 | kHz | Estimated Adapter Switching Frequency |
| P<sub>IN</sub> | Total Input Power | — | — | 54.08 | W | Combined Worst-Case Input Power |
| I<sub>IN</sub> | Input Current | — | — | 2.94 | A | Max Current Drawn from Adapter |
| I<sub>OUT</sub> | Output Load Current | — | — | 2.75 | A | Hardware Current Limit |
| C<sub>IN(EQ)</sub> | Equivalent Filter Capacitance | — | 120 | — | μF | Calculated Equivalent Input Capacitance |
| L<sub>IN</sub> | Input Filter Inductance | — | 6.8 | — | μH | Selected Power Inductor |
| R<sub>CS</sub> | Output Current Sense Resistor | — | 22 | — | mΩ | [See Calculations]( #output-shunt-resistor-rm-r_sout) |
| V<sub>CS(REF)</sub> | Reference for ADC | — | 3.025 | — | V | [See Calculations]( #output-shunt-resistor-rm-r_sout) |

### U1 - LM25117 Variables
| Variable | Description | MIN | TYP | MAX | UNIT | Source / Note |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| η<sub>(1)</sub> | Output Efficiency | 78 | 80 | 82 | % | Estimated Efficiency Range |
| V<sub>OUT(1)</sub> | Pre-regulator Output Voltage | 1.85 | — | 14.4 | V | V<sub>OUT</sub> + 0.6 V (LDO Headroom) |
| I<sub>OUT(1)</sub> | Output Load Current | — | — | 2.75 | A | Hardware Current Limit Boundary |
| f<sub>SW(1)</sub> | Switching Frequency | — | 435 | — | kHz | Desired Switching Frequency |
| R<sub>T(1)</sub> | Timer Resistor | — | 11 | — | kΩ | [See Calculations](#timer-resistor-rm-r_t1) |
| L<sub>O(1)</sub> | Output Inductor | — | 20 | — | μH | [See Calculations](#output-inductor-rm-l_o1) |
| C<sub>VCC(1)</sub> | VCC Input Capacitor | — | 1 | — | μF | Selected Standard Capacitor Value |
| R<sub>VIN(1)</sub> | VIN Input Resistor | — | TBD | — | mΩ | Optional Standard Value |
| C<sub>VIN(1)</sub> | VIN Input Capacitor | — | 0.47 | — | μF | Optional Standard Value |
| R<sub>S(1)</sub> | Current Sense Resistor (for CM pin) | — | 25 | — | mΩ | [See Calculations](#current-sense-resistor-rm-r_s1) |
| R<sub>RAMP(1)</sub> | Ramp Resistor | — | 82 | — | kΩ | [See Calculations](#ramp-resistor-and-capacitor-rm-r_ramp1-and-rm-c_ramp1) |
| C<sub>RAMP(1)</sub> | Ramp Capacitor | — | 1 | — | nF | Selected Standard Capacitor Value |
| R<sub>UV2(1)</sub> | UVLO Resistor 1 | — | 50 | — | kΩ | [See Calculations](#uvlo-divider-rm-r_uv11-and-rm-r_uv21) |
| R<sub>UV1(1)</sub> | UVLO Resistor 2 | — | 3.9 | — | kΩ | [See Calculations](#uvlo-divider-rm-r_uv11-and-rm-r_uv21) |
| C<sub>FT(1)</sub> | UVLO Filter Capacitor | — | 100 | — | pF | Selected Standard Capacitor Value |
| C<sub>SS(1)</sub> | Soft-Start Capacitor | — | 120 | — | nF | [See Calculations](#soft-start-capacitor-rm-c_ss1) |
| C<sub>RES(1)</sub> | Restart Capacitor | — | 1 | — | μF | [See Calculations](#restart-capacitor-rm-c_res1) |
| R<sub>FB1(1)</sub> | Feedback Resistor 1 | — | 1.1 | — | kΩ | [See Calculations](#output-voltage-divider-rm-r_fb21-and-rm-r_fb11) |
| R<sub>FB2(1)</sub> | Feedback Resistor 2 | — | 18.7 | — | kΩ | [See Calculations](#output-voltage-divider-rm-r_fb21-and-rm-r_fb11) |
| R<sub>COMP(1)</sub> | Loop Compensation Network | — | 140 | — | kΩ | [See Calculations](#loop-compensation-network-rm-c_comp1-rm-r_comp1-and-rm-c_hf1-1) |
| C<sub>COMP(1)</sub> | Loop Compensation Network | — | 8.2 | — | nF | [See Calculations](#loop-compensation-network-rm-c_comp1-rm-r_comp1-and-rm-c_hf1-1) |
| C<sub>HF(1)</sub> | Loop Compensation Network | — | TBD | — | nF | [See Calculations](#loop-compensation-network-rm-c_comp1-rm-r_comp1-and-rm-c_hf1-1) |

### U2 - MIC29302 Variables
| Variable | Description | MIN | TYP | MAX | UNIT | Source / Note |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |

### U4 - TPS54331 Variables
| Variable | Description | MIN | TYP | MAX | UNIT | Source / Note |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| V<sub>OUT(4)</sub> | Output Voltage | — | 12.0 | — | V | Supplied by V<sub>IN</sub> |
| I<sub>OUT(4)</sub> | Output Current | — | TBD | — | A | Estimated Max Load |
| η<sub>(4)</sub> | Output Efficiency | 70 | 72 | 74 | % | Estimated Efficiency Range |
| f<sub>SW(4)</sub> | Switching Frequency | — | 570 | — | kHz | Fixed Switching Frequency |

### U6 - TPS54332 Variables
| Variable | Description | MIN | TYP | MAX | UNIT | Source / Note |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| V<sub>OUT(6)</sub> | Output Voltage | — | 5.0 | — | V | Supplied by V<sub>IN</sub> |
| I<sub>OUT(6)</sub> | Output Current | — | TBD | — | A | Estimated Max Load |
| η<sub>(6)</sub> | Output Efficiency | 74 | 76 | 78 | % | Estimated Efficiency Range |
| f<sub>SW(6)</sub> | Switching Frequency | — | 1 | — | MHz | Fixed Switching Frequency |

*Note: Some of the components are To Be Determined [TBD] based on availability and final layout space constraints.*

## Math Calculations
### Stage 1: Power Input & Input Filter
#### Middlebrook Criteria Confirmation
To meet the Middlebrook criteria, input impedance of the converter must be at least 10x greater than output impedance of the source. To account for worst-case scenario, at lowest input impedance, minimum value of input voltage ($\rm V_{IN}$) was used.

*Note: Auxiliary rails are excluded from the calculations as they draw minimal power relative to the main rail.*

$$
\begin{aligned}
\rm P_{IN(1)} & = \rm \frac{I_{OUT(1)} \cdot V_{OUT(1)}}{\upeta_{(1)}}\ [W] \\
  & = \frac{2.75 \cdot 14.4}{0.78} \\
  \newline
  & \approx \rm 50.77\ W
\end{aligned}
$$

$$
\begin{aligned}
\rm Z_{IN} & = \rm \frac{V_{IN}^2}{P_{IN}}\ [\Omega] \\
  & = \frac{18.4^2}{50.77} \\
  \newline
  & \approx \rm 6.67\ \Omega
\end{aligned}
$$

For $\rm Z_{IN} \geq 10 \cdot Z_{OUT(FILTER)}$ to be true, output impedance of the source ($\rm Z_{OUT(FILTER)}$) must be less than $0.66\ \rm \Omega$. ($\rm L_{IN}$ was selected as standard value of 6.8 $\rm \upmu H$.)

$$
\begin{aligned}
\rm Z_{OUT(FILTER)} & = \rm \sqrt{\frac{L_{IN}}{C_{IN(EQ)}}}\ [\Omega] \\
  & = \sqrt{\frac{6.8 \cdot 10^{-6}}{120 \cdot 10^{-6}}} \\
  \newline
  & \approx \rm 0.24\ \Omega\ \(\text{27x less than}\ Z_{IN}\)
\end{aligned}
$$

#### Cut-off Frequency Confirmation
To reduce noise coupling at the input node, the cutoff frequency of the low-pass filter should be at least 10x lower than the switching frequency. 

For a conservative baseline, the nominal adapter switching frequency ($\rm f_{SW} \approx \rm 100 kHz$) was considered. Although adapters typically have relatively low output ripple, designing with a sufficiently low cut-off frequency increases attenuation of input ripple and suppress noise coupling between the other switching regulators connected to that node.

$$
\begin{aligned}
\rm f_{C} &= \rm \frac{1}{2 \uppi \sqrt{L_{IN} \cdot C_{IN(EQ)}}}\ [\rm Hz] \\
  & = \frac{1}{2 \uppi \sqrt{(6.8 \cdot 10^{-6}) \cdot (120 \cdot 10^{-6})}} \\
  \newline
  & \approx \rm 5.57\ kHz\ \(\text{17x less than}\ f_{SW}\)
\end{aligned}
$$

#### Input MOSFET Heat Dissipation
[TBD]

### Stage 2A: Main Adjustable Power Rail
#### Timer Resistor ($\rm R_{T(1)}$) 
The switching frequency of the main buck regulator was set to 435 kHz via the $R_{T}$ pin resistor; this enables sufficient separation from the adapter's lower switching frequency ($\approx 100\rm\ kHz$) to minimize beat frequency noise, while preventing excessive switching losses at higher frequencies.

$$
\begin{align*}
\rm R_{T(1)} & = \frac{5.2\cdot 10^9}{\rm f_{SW(1)}} - 948\ [\Omega] \\
  & = \frac{5.2\cdot 10^9}{435\rm\ kHz} - 948 \\
  \newline
  & \approx 11\rm\ k\Omega
\end{align*}
$$
  
$$
\boxed{
\begin{align*}
  &\text{Picked Value(s):} \\
  &\diamond \rm R_{T(1)} =\ 11\rm\ k\Omega
\end{align*}
}
$$

#### Output Inductor ($\rm L_{O(1)}$)
The output inductance was calculated using a nominal mid-range voltage of $\rm V_{OUT} = 8\rm\ V$ to achieve a balanced ripple current trade-off over the full output voltage range. In addition, maximum inductor ripple ($\rm I_{PP(1)}$) current was selected as 20% of the full load current.

$$
\begin{align*}
\rm L_{O(1)} & = \frac{\rm V_{OUT}}{\rm I_{PP(1)}\cdot \rm f_{SW(1)}}\cdot \left(1 - \frac{\rm V_{OUT}}{\rm V_{IN}}\right)\ [\rm H] \\
  & = \frac{8\rm\ V}{2.75\rm\ A \cdot 0.2 \cdot 435\ kHz}\cdot \left(1 - \frac{8\rm\ V}{20\rm\ V} \right) \\
  \newline
  & \approx 20.07\rm\ \upmu H
\end{align*}
$$
  
$$
\boxed{
\begin{align*}
  &\text{Picked Value(s):} \\
  &\diamond \rm L_{O(1)} =\ 20\rm\ \upmu H
\end{align*}
}
$$

#### Current Sense Resistor ($\rm R_{S(1)}$)
Maximum output current capability ($\rm I_{OUT(MAX)}$) was selected 150% of the full load current to account for tolerances.

$$
\begin{align*}
\rm R_{S(1)}  & = \frac{\rm V_{CS(TH)(1)}}{\rm I_{OUT(MAX)} + \left(\dfrac{\rm V_{OUT}\cdot \rm K}{\rm f_{SW(1)}\cdot L_{O(1)}}\right) - \left(\dfrac{\rm I_{PP(1)}}{2}\right)}\ [\Omega] \\ 
  & = \frac{0.12\rm\ V}{2.75\rm\ A \cdot 1.5 + \left(\dfrac{8\rm\ V\cdot 1}{435\rm\ kHz\cdot 20\ \upmu H}\right) - \left(\dfrac{0.55\rm\ A}{2}\right)} \\
  \newline
  & \approx 25.13\rm\ m\Omega \\
\rule{0pt}{50pt} \\
\rm P_{RS(1)} & = \left(1 - \frac{\rm V_{OUT}}{\rm{V_{IN}}}\right)\cdot (\rm I_{OUT})^2\cdot R_{S(1)}\ [\rm W] \\
  & = \left(1 - \frac{8\rm\ V}{20\rm\ V}\right)\cdot (2.75\rm\ A)^2\cdot 25\ m\Omega \\
  \newline
  & \approx 0.11\rm\ W
\end{align*}
$$

$$
\boxed{
\begin{align*}
  &\text{Picked Value(s):} \\
  &\diamond \rm R_{S(1)} = 25\rm\ m\Omega\ \\
  &\diamond \rm P_{RS(1)} = [TBD > 0.11W]
\end{align*}
}
$$

$\circ$ ***Note:*** Since the LM25117 uses an emulated current ramp, it samples the valley current just before the high-side switch turns on. This means the controller is unaffected by the large leading-edge switching spikes. Therefore, a current sense filter was not used in this design to avoid propagation delay on current sensing.

#### Ramp Resistor and Capacitor ($\rm R_{RAMP(1)}$ and $\rm C_{RAMP(1)}$)
Current sense amplifier gain ($\rm A_{S(1)}$) and K factor ($\rm K_{(1)}$) are both defined in the datasheet. K factor was set to 1 to prevent sub-harmonic oscillations and ensure one-cycle damping, as recommended in the datasheet.

$$
\begin{align*}
\rm R_{RAMP(1)} & = \frac{\rm L_{O(1)}}{\rm K_{(1)}\cdot C_{RAMP(1)}\cdot R_{S(1)}\cdot A_{S(1)}}\ [\Omega] \\
  & = \frac{20\rm\ \upmu H}{1\cdot 1\rm\ nF\cdot 25\ m\Omega\cdot 10} \\
  \newline
  & = 80\rm\ k\Omega
\end{align*}
$$

$$
\boxed{
\begin{align*}
  &\text{Picked Value(s):} \\
  &\diamond \rm C_{RAMP(1)} =\ 1\rm\ nF \\
  &\diamond \rm R_{RAMP(1)} =\ 82\rm\ k\Omega
\end{align*}
}
$$

$\circ$ ***Note:*** The value of $\rm C_{RAMP(1)}$ was set to the standard capacitor value of 1 nF.

#### UVLO Divider ($\rm R_{UV1(1)}$ and $\rm R_{UV2(1)}$)
The startup threshold (${\rm V_{STARTUP(1)}}$) was set to 17.4 V, with 1 V hysteresis (${\rm V_{HYS(1)}}$) using UVLO pin for undervoltage protection.

$$
\begin{align*}
\rm R_{UV2(1)} & = \frac{\rm V_{HYS(1)}}{20\rm\ \upmu A}\ [\Omega] \\
  & = \frac{1\rm\ V}{20\rm\ \upmu A} \\
  \newline
  & = 50\rm\ k\Omega \\
\rule{0pt}{50pt} \\
\rm R_{UV1(1)} & = \frac{1.25\rm\ V\cdot R_{UV2(1)}}{\rm V_{STARTUP(1)} - 1.25\ V}\ [\Omega] \\ 
  & = \frac{1.25\rm\ V\cdot 50\ k\Omega}{17.4\rm\ V - 1.25\ V} \\
  \newline
  & \approx 3.87\rm\ k\Omega
\end{align*}
$$

$$
\boxed{
\begin{align*}
  &\text{Picked Value(s):} \\
  &\diamond \rm R_{UV2(1)} =\ 50\rm\ k\Omega \\
  &\diamond \rm R_{UV1(1)} =\ 3.9\rm\ k\Omega \\
  &\diamond \rm C_{FT(1)}  =\ 100\rm\ pF
\end{align*}
}
$$

#### Soft-Start Capacitor ($\rm C_{SS(1)}$)
The soft-start time ($\rm t_{SS}$) was selected as 10 ms to mitigate high inrush currents at startup without accidentally activating the IC's protection circuitry.

$$
\begin{align*}
\rm C_{SS(1)} & = \frac{\rm t_{SS} \cdot 10\ \upmu A}{0.8\rm\ V}\ [\rm F] \\
  & = \frac{10\rm\ ms\cdot 10\ \upmu A}{0.8\rm\ V} \\
  \newline
  & = 125\rm\ nF
\end{align*}
$$

$$
\boxed{
\begin{align*}
  &\text{Picked Value(s):} \\
  &\diamond \rm C_{SS(1)} =\ 120\rm\ nF
\end{align*}
}
$$

#### Restart Capacitor ($\rm C_{RES(1)}$)
The restart delay ($\rm t_{RES}$) was set to 125 ms to allow sufficient cooling during a continuous fault condition, while keeping the system recovery reasonably fast.

$$
\begin{align*}
\rm C_{RES(1)} & = \frac{\rm t_{RES} \cdot 10\ \upmu A}{1.25\rm\ V}\ [\rm F] \\
  & = \frac{125\rm\ ms\cdot 10\ \upmu A}{1.25\rm\ V} \\
  \newline
  & = 1\rm\ uF 
\end{align*}
$$

$$
\boxed{
\begin{align*}
  &\text{Picked Value(s):} \\
  &\diamond \rm C_{RES(1)} =\ 1\rm\ uF
\end{align*}
}
$$

#### Output Voltage Divider ($\rm R_{FB2(1)}$ and $\rm R_{FB1(1)}$)
The feedback divider resistors were configured for the maximum output voltage (${\rm V_{OUT(1)}}$) to enable output voltage adjustment using a DAC-based feedback adjustment.

$$
\begin{align*}
\frac{\rm R_{FB2(1)}}{\rm R_{FB1(1)}} & = \frac{\rm\ V_{OUT(1)}}{0.8\rm\ V} - 1 \\
  & = \frac{14.4\rm\ V}{0.8\rm\ V} - 1 \\
  \newline
  & = 17 \\
\rule{0pt}{50pt} \\
\rm R_{FB2(1)} & = 17\cdot \rm R_{FB1(1)} \\
\end{align*}
$$

$$
\boxed{
\begin{align*}
  &\text{Picked Value(s):} \\
  &\diamond \rm R_{FB2(1)} =\ 18.7\rm\ k\Omega \\
  &\diamond \rm R_{FB1(1)} =\ 1.1\rm\ k\Omega \\
\end{align*}
}
$$

#### Loop Compensation Network ($\rm C_{COMP(1)}$, $\rm R_{COMP(1)}$ and $\rm C_{HF(1)}$)
The loop bandwidth ($\rm f_{CROSS(1)}$) was set to 1/20 of the switching frequency ($\rm f_{SW(1)}$) to prioritize loop stability over aggressive transient speed. This additionally prevents $\rm R_{COMP(1)}$ from reaching excessively high values, thus ensuring better noise immunity.

$$
\begin{align*}
\rm f_{CROSS(1)} & = \frac{\rm f_{SW(1)}}{20}\ [\rm Hz] \\
  \newline
  & = 21.75\rm kHz \\
\rule{0pt}{50pt} \\
\rm R_{COMP(1)}  & = \rm 2\uppi\cdot R_{S(1)}\cdot A_{S(1)}\cdot C_{OUT(1)}\cdot R_{FB2(1)}\cdot f_{CROSS(1)}\ [\Omega] \\
  & = \rm 2\uppi\cdot 25 m\Omega\cdot 10\cdot 220 \upmu F\cdot 18.7\ k\Omega\cdot 21.75\ kHz \\
  \newline
  & \approx 140.6\rm\ k\Omega \\
\rule{0pt}{50pt} \\
\rm C_{COMP(1)}  & = \frac{\rm R_{LOAD}\cdot \rm C_{OUT}}{\rm R_{COMP}}\ [\rm F] \\
  & = \frac{\rm \left(\dfrac{14.4\rm\ V}{2.75\rm\ A}\right)\cdot 220\rm\ \upmu F}{\rm 140\rm\ k\Omega} \\
  \newline
  & \approx 8.23\rm\ nF \\
\rule{0pt}{50pt} \\
\rm C_{HF} & =\ \text{[TBD]}
\end{align*}
$$

$$
\boxed{
\begin{align*}
  &\text{Picked Value(s):} \\
  &\diamond \rm R_{COMP(1)} =\ 140\rm\ k\Omega \\
  &\diamond \rm C_{COMP(1)} =\ 8.2\rm\ nF \\
\end{align*}
}
$$

#### Output Shunt Resistor ($\rm R_{CS}$)
The output current was monitored by converting the load current ($\rm I_{OUT(1)}$) into an analog voltage signal via a dedicated shunt resistor and a current sense amplifier. The resulting analog signal was then digitized by the MCU's ADC. Since the LDO input current is approximately equal to its output current, the shunt resistor was placed before the feedback node at the LDO input to prevent the voltage drop across the shunt resistor from affecting the regulated output voltage.

As low power consumption was not a primary concern for this project, the amplifier gain ($\rm A_{CS}$) was set to 50x to minimize the amplification of measurement errors. In addition, the reference voltage ($\rm V_{CS(REF)}$) was limited to 3.0 V, leaving 0.3 V headroom below the MCU supply voltage to reduce the impact of possible control errors.

$$
\begin{align*}
\rm R_{CS} & = \rm \frac{\rm V_{CS(REF)} / A_{CS}}{\rm I_{OUT(MAX)}}\ [\Omega] \\
  & = \frac{3.0\rm\ V / 50}{2.75\rm\ A} \\
  \newline
  & \approx 21.82\rm\ m\Omega \\
\end{align*}
$$

To adjust reference voltage with the closest standard value for the shunt resistor:

$$\rm V_{CS(REF)} = \rm 3\cdot\frac{22\cdot 10^{-3}}{21.82\cdot 10^{-3}} = 3.025\rm\ V$$

$$
\boxed{
\begin{align*}
  &\text{Picked Value(s):} \\
  &\diamond \rm R_{CS} =\ 22\rm\ m\Omega \\
  &\diamond \rm P_{RCS} =\ \rm [TBD > 0.17\ W] \\
  &\diamond \rm A_{CS} =\ 50\rm x \\
  &\diamond \rm V_{CS(REF)} =\ 3.025\rm\ V
\end{align*}
}
$$
