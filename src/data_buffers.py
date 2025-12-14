"""
Data Buffer Management

Maintains rolling buffers for time-series plotting
of gas concentration values.
"""

from collections import deque
from gas_constants import GAS_CURVES

BUFFER_SIZE = 50
timestamps = deque([0]*BUFFER_SIZE, maxlen=BUFFER_SIZE)
data_buffers = {gas: deque([0]*BUFFER_SIZE, maxlen=BUFFER_SIZE) for gas in GAS_CURVES}

def update_buffers(sample, ppm_values):
    timestamps.append(sample)
    for gas in ppm_values:
        data_buffers[gas].append(ppm_values[gas])
    return timestamps, data_buffers

