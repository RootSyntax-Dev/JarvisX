# gui.py — JarvisX Smart Edition ⚡

import tkinter as tk
from tkinter import scrolledtext
import threading, time, os, psutil, webbrowser
import datetime, wikipedia, pywhatkit, pyjokes

from voice import speak, stop_speak
from listen import listen


# ================= WINDOW SETUP =================

root = tk.Tk()
root.title("Jarvis X")
root.geometry("950x650")
root.configure(bg="#0C0C0C")


title = tk.Label(
    root,
    text="Jarvis X",
    bg="#0C0C0C",
    fg="#00FFAA",
    font=("Consolas", 30, "bold"),
)
title.pack(pady=(15, 5))


separator = tk.Frame(root, bg="#00FFAA", height=2)
separator.pack(fill=tk.X, padx=60, pady=(0, 10))


console = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    width=95,
    height=26,
    bg="#000",
    fg="#00FFAA",
    insertbackground="#00FFAA",
    font=("Consolas", 12),
    relief="flat",
)
console.pack(fill=tk.BOTH, expand=True, padx=30, pady=(10, 10))


def log_user(text):
    console.insert(tk.END, f"🧑 You: {text}\n", "user")
    console.see(tk.END)


def log_jarvis(text):
    console.insert(tk.END, f"🤖 Jarvis: {text}\n", "jarvis")
    console.see(tk.END)


console.tag_config("user", foreground="#00FFAA")
console.tag_config("jarvis", foreground="#00BFFF")


def reply(text):
    time.sleep(0.6)   # 🔥 allow mic to release
    speak(text)
    log_jarvis(text)


# ================= LISTENING ANIMATION =================

canvas = tk.Canvas(root, width=120, height=120, bg="#0C0C0C", highlightthickness=0)
canvas.pack(pady=5)
ring = canvas.create_oval(10, 10, 110, 110, outline="#00FFAA", width=4)


def animate_ring():
    while listening_flag:
        for i in range(2, 8):
            canvas.itemconfig(ring, width=i)
            canvas.update()
            time.sleep(0.03)
        for i in range(8, 2, -1):
            canvas.itemconfig(ring, width=i)
            canvas.update()
            time.sleep(0.03)


# ================= APP OPENER =================

def find_and_open_app(app_name):
    app_name = app_name.lower().replace("open", "").strip()
    reply(f"Opening {app_name}...")

    # 🌐 Websites
    if "youtube" in app_name:
        webbrowser.open("https://youtube.com")
        return True
    if "google" in app_name:
        webbrowser.open("https://google.com")
        return True

    # 🪟 Built-in Windows apps
    system_apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "cmd": "cmd.exe",
        "explorer": "explorer.exe",
    }

    for key, exe in system_apps.items():
        if key in app_name:
            os.system(exe)
            return True

    # 🖥️ Installed desktop apps (common paths)
    program_dirs = [
        r"C:\Program Files",
        r"C:\Program Files (x86)",
        os.path.expandvars(r"%LOCALAPPDATA%"),
    ]

    for folder in program_dirs:
        for root_dir, _, files in os.walk(folder):
            for file in files:
                if app_name in file.lower() and file.endswith(".exe"):
                    try:
                        os.startfile(os.path.join(root_dir, file))
                        return True
                    except:
                        pass

    # 🌍 Fallback
    webbrowser.open(f"https://www.google.com/search?q={app_name}")
    reply(f"Couldn't find {app_name}, searched online.")
    return False

# ================= MAIN LOGIC =================

listening_flag = True
active = True


def jarvis_brain():
    global listening_flag, active

    reply("Jarvis X online and ready for commands.")

    while active:
        try:
            if listening_flag:

                # Start animation once
                if not getattr(root, "ring_running", False):
                    root.ring_running = True
                    threading.Thread(target=animate_ring, daemon=True).start()

                query = listen()
                time.sleep(0.5)

                if not query:
                    continue

                query = query.lower().strip()
                log_user(query)

                query = query.replace("jarvis", "").strip()

                # ===== CONTROL =====
                if "stop listening" in query:
                    reply("Paused listening.")
                    listening_flag = False
                    continue

                elif "start listening" in query or "resume" in query:
                    reply("Listening resumed.")
                    listening_flag = True
                    continue

                elif any(word in query for word in ["exit", "shutdown", "quit"]):
                    reply("Goodbye Vinay.")
                    active = False
                    stop_speak()
                    root.quit()
                    break

                # ===== TIME / SYSTEM =====
                elif "time" in query:
                    now = datetime.datetime.now().strftime("%I:%M %p")
                    reply(f"The time is {now}")

                elif "date" in query:
                    date = datetime.datetime.now().strftime("%d %B %Y")
                    reply(f"Today is {date}")

                elif "battery" in query:
                    battery = psutil.sensors_battery()
                    if battery:
                        reply(f"Battery at {battery.percent} percent")
                    else:
                        reply("Battery info unavailable")

                elif "cpu" in query:
                    cpu = psutil.cpu_percent()
                    reply(f"CPU usage at {cpu} percent")

                # ===== APPS =====
                elif any(word in query for word in ["open", "start", "launch"]):
                    find_and_open_app(query)

                # ===== SEARCH =====
                elif "search" in query:
                    topic = query.replace("search", "").strip()
                    reply(f"Searching {topic}")
                    pywhatkit.search(topic)

                # ===== FUN =====
                elif "joke" in query:
                    reply(pyjokes.get_joke())

                # ===== WIKIPEDIA =====
                elif any(x in query for x in ["who is", "what is", "tell me about"]):
                    topic = (
                        query.replace("who is", "")
                        .replace("what is", "")
                        .replace("tell me about", "")
                        .strip()
                    )
                    try:
                        info = wikipedia.summary(topic, 1)
                        reply(info)
                    except:
                        reply("Sorry, I couldn’t find that.")

                # ===== GREETINGS =====
                elif any(x in query for x in ["hello", "hi", "hey"]):
                    reply("Hello Vinay, how can I help you?")

                elif "how are you" in query or "how r u" in query:
                    reply("I am functioning perfectly.")

                elif "what are you doing" in query or "what r u doing" in query:
                    reply("I am waiting for your command.")

                elif "your name" in query:
                    reply("I am Jarvis X, your personal assistant.")

                else:
                    reply("Sorry, I didn’t understand that.")

            else:
                time.sleep(1)

        except Exception as e:
            reply(f"Error: {e}")


# ================= START =================

if __name__ == "__main__":
    threading.Thread(target=jarvis_brain, daemon=True).start()
    root.mainloop()