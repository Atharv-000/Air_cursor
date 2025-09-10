import speech_recognition as sr
import subprocess

WAKE_WORD = "phantom"

def listen_for_wake_word():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake word...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio).lower()
            print("Heard:", text)
            return WAKE_WORD in text
        except sr.UnknownValueError:
            return False
        except sr.RequestError as e:
            print("Could not request results:", e)
            return False

if __name__ == "__main__":
    while True:
        if listen_for_wake_word():
            print("✅ Wake word detected! Launching AirCursor...")
            subprocess.call(["python", "main.py"])
            break
