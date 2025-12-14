"""
Smart Air Purifier – GUI Dashboard
Platform: Raspberry Pi Zero

Description:
Tkinter-based graphical dashboard for monitoring air quality,
visualizing gas concentration levels, logging sensor data,
and interacting with a voice assistant module.

Status:
Prototype tested on Raspberry Pi.
"""
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import subprocess
import os

from sensor_read import read_voltage, get_ppm, log_to_csv
from data_buffers import update_buffers, timestamps, data_buffers
from gas_constants import GAS_CURVES

# Thresholds
THRESHOLDS = {
    "CO₂": 1000,
    "NH₃": 25,
    "NOx": 40,
}

# State
sample = 0
is_paused = False
ripple_active = False

# Root window
root = tk.Tk()
root.title("SORA_TYPE 1 AIR QUALITY DASHBOARD")
root.configure(bg="#0a0f1c")
root.geometry("800x700")

# Style
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#0a0f1c", foreground="#00ffff", font=("Consolas", 12))
style.configure("TButton", background="#1a1f2c", foreground="#00ffff", font=("Consolas", 10))

# Title panel
title_frame = tk.Frame(root, bg="#1a1f2c")
title_frame.pack(pady=(10, 0))
tk.Label(title_frame, text="SORA_TYPE 1", font=("Consolas", 20, "bold"), fg="#00ffff", bg="#1a1f2c").pack()
tk.Label(title_frame, text="AIR QUALITY DASHBOARD", font=("Consolas", 14), fg="#00ffff", bg="#1a1f2c").pack()

# Graph panel
graph_frame = tk.Frame(root, bg="#1a1f2c")
graph_frame.pack(pady=5)

fig, ax = plt.subplots(figsize=(6, 3.5))
fig.patch.set_facecolor("#0a0f1c")
ax.set_facecolor("#0a0f1c")

neon_colors = {
    "CO₂": "#00ffff",
    "NH₃": "#1f77ff",
    "NOx": "#00ff99"
}

lines = {}
for gas in GAS_CURVES:
    lines[gas], = ax.plot([], [], label=gas, color=neon_colors[gas], linewidth=2)

ax.grid(True, color="#00ffff", alpha=0.2)
ax.set_ylim(0, 1200)
ax.set_xlim(0, 50)
ax.set_ylabel("ppm", color="#00ffff", fontsize=10)
ax.set_xlabel("Time (samples)", color="#00ffff", fontsize=10)
ax.tick_params(colors="#00ffff")
ax.spines["bottom"].set_color("#00ffff")
ax.spines["left"].set_color("#00ffff")
ax.legend(facecolor="#1a1f2c", edgecolor="#00ffff", labelcolor="#00ffff")

canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().pack()

# Status panel
status_frame = tk.Frame(root, bg="#1a1f2c")
status_frame.pack(pady=5)

ppm_labels = {}
for gas in GAS_CURVES:
    lbl = ttk.Label(status_frame, text=f"{gas}: 0 ppm", style="TLabel")
    lbl.pack(side=tk.LEFT, padx=10)
    ppm_labels[gas] = lbl

warning_label = ttk.Label(root, text="", style="TLabel", foreground="#ff00ff")
warning_label.pack(pady=5)

# Control panel
control_frame = tk.Frame(root, bg="#1a1f2c")
control_frame.pack(pady=5)

def toggle_pause():
    global is_paused
    is_paused = not is_paused
    pause_button.config(text="Resume" if is_paused else "Pause")

pause_button = ttk.Button(control_frame, text="Pause", command=toggle_pause, style="TButton")
pause_button.pack(side=tk.LEFT, padx=10)

def open_log_folder():
    subprocess.Popen(["xdg-open", "/home/pi/Desktop/SORA_TYPE1/logs"])

open_button = ttk.Button(control_frame, text="Open Log Folder", command=open_log_folder, style="TButton")
open_button.pack(side=tk.LEFT, padx=10)

# Voice assistant bubble
bubble_frame = tk.Frame(root, bg="#0a0f1c")
bubble_frame.pack(pady=5)

bubble_canvas = tk.Canvas(bubble_frame, width=160, height=160, bg="#0a0f1c", highlightthickness=0)
bubble_canvas.pack()

bubble = bubble_canvas.create_oval(40, 40, 120, 120, fill="#00ffff", outline="#00ffff", width=2)
bubble_text = bubble_canvas.create_text(80, 80, text="SORA", fill="#0a0f1c", font=("Consolas", 14, "bold"))

transcript_label = tk.Label(bubble_frame, text="", font=("Consolas", 10), fg="#00ffff", bg="#0a0f1c", wraplength=140, justify="center")
transcript_label.pack(pady=2)

ripple_rings = []
waveform = []

def animate_ripples():
    if not ripple_active:
        return
    for ring in ripple_rings:
        bubble_canvas.delete(ring)
    ripple_rings.clear()
    for i in range(3):
        radius = 40 + i * 15
        ring = bubble_canvas.create_oval(
            80 - radius, 80 - radius,
            80 + radius, 80 + radius,
            outline="#00ffff", width=1
        )
        ripple_rings.append(ring)
    root.after(500, animate_ripples)

def animate_waveform():
    for bar in waveform:
        bubble_canvas.delete(bar)
    waveform.clear()
    for i in range(5):
        x = 50 + i * 10
        height = 20 + (i % 3) * 10
        bar = bubble_canvas.create_line(x, 100, x, 100 - height, fill="#00ffff", width=2)
        waveform.append(bar)

def pulse():
    current_color = bubble_canvas.itemcget(bubble, "fill")
    new_color = "#1f1f1f" if current_color == "#00ffff" else "#00ffff"
    bubble_canvas.itemconfig(bubble, fill=new_color, outline=new_color)
    root.after(500, pulse)

pulse()

def update_transcript():
    try:
        with open("sora_transcript.txt", "r") as f:
            transcript = f.read()
        with open("sora_response.txt", "r") as f:
            response = f.read()
        transcript_label.config(text=f"You said:\n{transcript}\n\nSORA:\n{response}")
    except:
        pass
    root.after(2000, update_transcript)

update_transcript()

def check_listening():
    global ripple_active
    if os.path.exists("sora_listening.txt"):
        if not ripple_active:
            ripple_active = True
            animate_ripples()
        print("🎙️ SORA is listening…")
        animate_waveform()
    else:
        ripple_active = False
        for ring in ripple_rings:
            bubble_canvas.delete(ring)
        ripple_rings.clear()
        for bar in waveform:
            bubble_canvas.delete(bar)
        waveform.clear()
    root.after(1000, check_listening)

check_listening()

# Update loop
def update():
    global sample
    if not is_paused:
        try:
            voltage = read_voltage()
            sample += 1
            ppm_values = get_ppm(voltage)
            log_to_csv(voltage, ppm_values)

            print(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Voltage: {voltage:.3f} V")
            for gas, ppm in ppm_values.items():
                print(f"{gas}: {ppm} ppm", end="  ")
            print()

            ts, buffers = update_buffers(sample, ppm_values)
            for gas in GAS_CURVES:
                ppm = ppm_values[gas]
                ppm_labels[gas].config(
                    text=f"{gas}: {ppm} ppm",
                    foreground="#ff00ff" if ppm > THRESHOLDS[gas] else "#00ffff"
                )
                lines[gas].set_xdata(ts)
                lines[gas].set_ydata(buffers[gas])

            warnings = [f"{gas} high!" for gas, ppm in ppm_values.items() if ppm > THRESHOLDS[gas]]
            warning_label.config(text=" | ".join(warnings) if warnings else "")

            ax.relim()
            ax.autoscale_view()
            canvas.draw()
        except Exception as e:
            print("Sensor error:", e)

    root.after(2000, update)

# Launch voice assistant
try:
    subprocess.Popen(["python3", "voice_assistant.py"], cwd=os.path.dirname(__file__))
    print("🎙️ Voice assistant launched.")
except Exception as e:
    print("Failed to launch voice assistant:", e)

# Launch GUI
update()
root.mainloop()

