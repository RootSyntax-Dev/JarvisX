# jarvis.py
# Main command logic for Jarvis 2.0

import datetime
import webbrowser
import wikipedia
import pywhatkit
import pyjokes
from speak import speak
from listen import listen

def run_jarvis():
    speak("Hi, I am Jarvis 2 point O, your personal assistant.")
    while True:
        query = listen()

        if not query:
            continue

        if "time" in query:
            time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {time}")

        elif "date" in query:
            date = datetime.datetime.now().strftime("%d %B %Y")
            speak(f"Today's date is {date}")

        elif "open youtube" in query:
            speak("Opening YouTube")
            webbrowser.open("https://youtube.com")

        elif "open google" in query:
            speak("Opening Google")
            webbrowser.open("https://google.com")

        elif "search" in query:
            speak("Searching the web")
            pywhatkit.search(query.replace("search", ""))

        elif "who is" in query or "what is" in query:
            topic = query.replace("who is", "").replace("what is", "")
            try:
                info = wikipedia.summary(topic, 1)
                speak(info)
            except:
                speak("Couldn't find details about that.")

        elif "joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)

        elif "stop" in query or "exit" in query or "quit" in query:
            speak("Goodbye! Have a nice day.")
            break

        else:
            speak("Sorry, I don’t understand that command.")
if __name__ == "__main__":
    run_jarvis()
