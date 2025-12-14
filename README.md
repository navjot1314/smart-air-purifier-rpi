# Smart Air Purifier using Raspberry Pi Zero

## Overview
The Smart Air Purifier project is designed to monitor indoor environmental
conditions and automatically control an air purifier based on sensor readings.
The system is built using a Raspberry Pi Zero and environmental sensors, making
it suitable for low-power and continuous monitoring applications.

## Problem Statement
Indoor air pollution and poor ventilation can negatively affect health.
Traditional air purifiers often operate continuously without considering
actual air quality or environmental conditions. This project aims to improve
efficiency by enabling sensor-based intelligent control.

## System Description
The system continuously reads data from environmental sensors such as
temperature and air quality sensors. Based on predefined threshold values,
the Raspberry Pi Zero decides whether to activate or deactivate the air purifier.

## System Architecture
The Smart Air Purifier system is centered around a Raspberry Pi Zero that acts as
the main controller. Environmental sensors continuously provide data to the
controller, which processes the readings and controls the air purifier based on
predefined threshold values.

### Main Components
- Raspberry Pi Zero: Central controller and decision-making unit
- Temperature Sensor: Measures ambient temperature
- Air Quality Sensor: Detects pollution levels in the air
- Air Purifier / Fan Module: Activated or deactivated based on sensor data

### Working Flow
1. Sensors collect environmental data.
2. Raspberry Pi Zero reads sensor values using Python scripts.
3. Sensor values are compared against threshold limits.
4. The air purifier is turned ON or OFF accordingly.
5. The process repeats continuously for real-time monitoring.


## Technologies Used
- Raspberry Pi Zero
- Python
- Temperature Sensor
- Air Quality Sensor
- Linux (Raspberry Pi OS)

## Key Features
- Real-time environmental monitoring
- Automated air purifier control
- Threshold-based decision logic
- Low-power Raspberry Pi Zero platform
- Modular Python-based implementation

## Project Status
Hardware setup completed. Software implementation in progress.

## Future Enhancements
- Mobile or web-based monitoring dashboard
- Data logging and visualization
- Support for additional environmental sensors
- Advanced control logic for energy optimization
