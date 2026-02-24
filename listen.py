# listen.py — Jarvis X Speech Recognition

import sounddevice as sd
import numpy as np
import io
import wavio
import speech_recognition as sr
from voice import speak


def record_audio(duration=5, samplerate=16000):
    print("🎧 Listening...")

    try:
        recording = sd.rec(
            int(duration * samplerate),
            samplerate=samplerate,
            channels=1,
            dtype="float32",
        )
        sd.wait()
        print("✅ Recording complete.")
        return np.squeeze(recording)

    except Exception as e:
        print("Mic error:", e)
        speak("Microphone error")
        return None


def recognize_online(audio_data, samplerate=16000):
    try:
        wav_bytes = io.BytesIO()
        wavio.write(wav_bytes, audio_data, samplerate, sampwidth=2)
        wav_bytes.seek(0)

        r = sr.Recognizer()
        with sr.AudioFile(wav_bytes) as source:
            audio = r.record(source)

        print("🧠 Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print("✅ Recognized:", query)
        return query.lower()

    except:
        speak("Sorry, I didn't catch that")
        return ""


def listen():
    audio_data = record_audio()
    if audio_data is None:
        return ""

    return recognize_online(audio_data)