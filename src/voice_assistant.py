"""
Voice Assistant Module

Simulates a simple voice assistant interaction
for the Smart Air Purifier system.
"""

import openai
import speech_recognition as sr
import pyttsx3
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

from data_buffers import data_buffers

# === OpenAI Setup ===
openai.api_key = "sk-proj-..."

# === Spotify Setup ===
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="...",
    client_secret="...",
    redirect_uri="http://localhost:8888/callback",
    scope="user-read-playback-state,user-modify-playback-state,user-read-currently-playing"
))

# === Speech Engine ===
engine = pyttsx3.init()
engine.setProperty("rate", 180)
engine.setProperty("voice", engine.getProperty("voices")[0].id)

def speak(text):
    print("🧠 Assistant:", text)
    engine.say(text)
    engine.runAndWait()
    try:
        with open("sora_response.txt", "w") as f:
            f.write(text)
    except:
        pass

def get_sensor_summary():
    summary = {}
    for gas, buffer in data_buffers.items():
        values = list(buffer)
        if values:
            summary[gas] = {
                "latest": round(values[-1], 2),
                "max": round(max(values), 2),
                "min": round(min(values), 2),
                "avg": round(sum(values) / len(values), 2)
            }
    return summary

def ask_openai(query, sensor_data):
    prompt = f"""
You are SORA, a voice assistant for an air quality dashboard running on Raspberry Pi.
You have access to live sensor data and can control Spotify playback.
Here is the latest sensor summary:
{sensor_data}

User said: "{query}"
Respond naturally using the data above.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def run_voice_assistant():
    try:
        with open("sora_listening.txt", "w") as f:
            f.write("listening")
    except:
        pass

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening for command...")
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio).lower()
            print("🗣️ You said:", query)
            with open("sora_transcript.txt", "w") as f:
                f.write(query)
            sensor_data = get_sensor_summary()
            response = ask_openai(query, sensor_data)
            speak(response)
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
        except sr.RequestError:
            speak("Speech service is unavailable.")

    try:
        os.remove("sora_listening.txt")
    except:
        pass

def wait_for_hotword():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🔊 Waiting for hotword 'SORA'...")
        while True:
            audio = recognizer.listen(source)
            try:
                transcript = recognizer.recognize_google(audio).lower()
                print("🗣️ Heard:", transcript)
                if "sora" in transcript:
                    speak("Yes, Alligator?")
                    with open("sora_transcript.txt", "w") as f:
                        f.write(transcript)
                    run_voice_assistant()
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                speak("Speech service is unavailable.")

wait_for_hotword()

