import speech_recognition as sr
import subprocess
import os
import sys

WAKE_WORD = "start aircursor"

def listen_for_command():
recognizer = sr.Recognizer()
mic = sr.Microphone()

print("🎤 Voice Trigger Ready. Say 'start aircursor' to activate...")

with mic as source:
    recognizer.adjust_for_ambient_noise(source)

while True:
    try:
        with mic as source:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5)
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")

        if WAKE_WORD in command:
            print("✅ Wake word detected! Launching AirCursor...")
            launch_aircursor()
            break

    except sr.WaitTimeoutError:
        continue
    except sr.UnknownValueError:
        continue
    except sr.RequestError as e:
        print(f"API error: {e}")
        break


def launch_aircursor():
script_path = os.path.join(os.path.dirname(file), "main.py")
subprocess.Popen([sys.executable, script_path])

if name == "main":
listen_for_command()
