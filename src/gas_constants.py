"""
Gas Constants and Curves

Defines supported gases and basic curve identifiers
used for plotting and ppm calculation.
"""

GAS_CURVES = {
    "CO₂": "carbon_dioxide",
    "NH₃": "ammonia",
    "NOx": "nitrogen_oxides"
}
# Calibration constants
RLOAD = 10.0
RZERO = 76.63
ADC_VREF = 5.0

# Gas curves: (PARA, PARB)
GAS_CURVES = {
    "CO₂": (116.6020682, -2.769034857),
    "NH₃": (102.2, -2.473),
    "NOx": (33.7, -2.18),
}
