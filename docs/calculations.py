import os
import math
import numpy as np

if not os.path.exists('images'):
    os.makedirs('images')


# Board-level parameters
v_in = 20.0             # V
v_out_min = 1.25        # V
v_out_max = 13.8        # V
v_ldo_dropout = 0.6     # V
i_out = 2.75            # A
i_out_max = 2.75 * 1.5  # A


# U1 - LM25117 parameters
v_out_typ = 8.0         # V
i_pp_u1 = 2.75 * 0.2    # A
f_sw_u1 = 435e3         # Hz
t_ss_u1 = 10e-3         # ms
t_res_u1 = 125e-3       # ms
targ_v_s_ref = 3.0     # V
a_s = 50               # x

# Timer Resistor - Rt(U1)
calc_r_t_u1 = (5.2e9 / f_sw_u1) - 949  # Ohms
r_t_u1 = 11e3
# print(f"\nTimer Resistor:\t Rt(U1): {calc_r_t_u1 * 1e-3:.2f} kOhms")

# Output Inductor - Lo(U1)
calc_l_o_u1 = (v_out_typ / (i_pp_u1 * f_sw_u1)) * (1 - (v_out_typ / v_in))  # H
l_o_u1 = 20e-6
# print(f"\nOutput Inductor:\t Lo(U1): {calc_l_o_u1 * 1e6:.2f} uH")

# Current Sense Resistor - Rcs(U1)
calc_r_cs_u1 = 0.12 / (i_out_max + ((v_out_typ * 1) / (f_sw_u1 * l_o_u1)) - (i_pp_u1 / 2))  # Ohms
r_cs_u1  = 25e-3
calc_p_rcs_u1 = (1 - (v_out_min / (v_in + v_ldo_dropout))) * (i_out ** 2) * r_cs_u1  # W
p_rcs_u1 = calc_p_rcs_u1
# print(f"\nCurrent Sense Resistor:\t Rs(U1): {calc_r_cs_u1 * 1e3:.2f} mOhms | Prs(U1): {calc_p_rcs_u1:.2f} W")

# Ramp Resistor and Capacitor - Rramp(U1) and Cramp(U1)
c_ramp_u1 = 1e-9
calc_r_ramp_u1 = l_o_u1 / (1 * c_ramp_u1 * r_cs_u1 * 10)
r_ramp_u1 = 80e3
print(f"\nRamp Resistor:\t Rramp(U1): {calc_r_ramp_u1 * 1e-3:.2f} kOhms")

# Output Shunt Resistor - Rs
calc_r_s = (targ_v_s_ref / a_s) / i_out  # Ohms
r_s = 22e-3
v_s_ref = (r_s * i_out) * a_s  # V
calc_p_rs = (i_out ** 2) * r_s  # W
p_rs = calc_p_rs 
# print(f"Output Current Sense Resistor:\t Rcs: {calc_r_cs * 1e3:.2f} mOhms | Prcs: {calc_p_rcs:.2f} W | Updated VcsRef: {v_cs_ref} V")


# Latex Variable File (variables.tex)
latex_variables = {
    "Vin": v_in,
    "VoutMin": v_out_min,
    "VoutMax": v_out_max,
    "VldoDropout": v_ldo_dropout,
    "Iout": i_out,
    "IoutMax": i_out_max,
    "VoutTyp": v_out_typ,
    "IppA": i_pp_u1,
    "fswA": f_sw_u1,
    "tssA": t_ss_u1,
    "tresA": t_res_u1,
    "CalcRtA": calc_r_t_u1,
    "RtA": r_t_u1,
    "CalcLoA": calc_l_o_u1,
    "LoA": l_o_u1,
    "CalcRcsA": calc_r_cs_u1,
    "RcsA": r_cs_u1,
    "CalcPrcsA": calc_p_rcs_u1,
    "PrcsA": p_rcs_u1,
    "CrampA": c_ramp_u1,
    "CalcRrampA": calc_r_ramp_u1,
    "RrampA": r_ramp_u1,
    "As": a_s,
    "CalcRs": calc_r_s,
    "Rs": r_s,
    "TargVsRef": targ_v_s_ref,
    "VsRef": v_s_ref,
    "CalcPrs": calc_p_rs,
    "Prs": p_rs
}

with open("variables.tex", "w") as f:
    for var_name, var_value in latex_variables.items():
        f.write(f"\\newcommand{{\\{var_name}}}{{{var_value}}}\n")