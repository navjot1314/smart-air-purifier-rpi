"""
Sensor Reading Module

Handles voltage reading, gas concentration calculation,
and logging sensor data to CSV.
"""
import board
import busio
import csv
import os
from datetime import datetime
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from gas_constants import RLOAD, RZERO, ADC_VREF, GAS_CURVES

# Create logs folder if it doesn't exist
LOG_FOLDER = "/home/pi/Desktop/SORA_TYPE1/logs"
os.makedirs(LOG_FOLDER, exist_ok=True)

def get_log_file_path():
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(LOG_FOLDER, f"log_{today}.csv")

# Initialize I2C and ADS1115
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P0)

def read_voltage():
    """Reads the current voltage from the MQ135 sensor via ADS1115."""
    return chan.voltage

def get_ppm(voltage):
    """Converts voltage to ppm values for each gas using calibration curves."""
    ppm_values = {}
    for gas, (para, parb) in GAS_CURVES.items():
        if voltage <= 0:
            ppm = 0
        else:
            resistance = ((ADC_VREF * RLOAD) / voltage) - RLOAD
            ratio = resistance / RZERO
            ppm = round(para * (ratio ** parb), 2)
        ppm_values[gas] = ppm
    return ppm_values

def log_to_csv(voltage, ppm_values, filename=None):
    """Logs timestamp, voltage, and ppm values to a CSV file."""
    if filename is None:
        filename = get_log_file_path()

    try:
        # Create file with header if it doesn't exist
        with open(filename, 'x', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Voltage"] + list(ppm_values.keys()))
    except FileExistsError:
        pass

    # Append new row
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            f"{voltage:.3f}"
        ] + [ppm_values[gas] for gas in ppm_values])

