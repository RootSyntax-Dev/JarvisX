# voice.py — Jarvis X Speech Engine

import pyttsx3
import threading
import sys

_engine = None
_engine_lock = threading.Lock()


def _init_engine():
    global _engine
    if _engine is not None:
        return

    try:
        _engine = pyttsx3.init()
        _engine.setProperty("rate", 170)
        _engine.setProperty("volume", 1.0)
        print("🔊 Voice engine initialized.")
    except Exception as e:
        print("❌ TTS init failed:", e, file=sys.stderr)
        _engine = None


def speak(text):
    if not text:
        return

    def _run():
        global _engine

        with _engine_lock:
            _init_engine()
            if _engine is None:
                print("[TTS unavailable]", text)
                return

            try:
                print(f"🤖 Speaking: {text}")
                _engine.stop()
                _engine.say(text)
                _engine.runAndWait()
            except Exception as e:
                print("TTS error:", e)

    # 🔥 Run speech in separate thread
    threading.Thread(target=_run, daemon=True).start()


def stop_speak():
    global _engine
    try:
        if _engine:
            _engine.stop()
    except Exception as e:
        print("stop_speak error:", e)