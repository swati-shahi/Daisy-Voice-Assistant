import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import pyjokes
import os
import pyautogui

# Initialize speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice

# Speak function
def speak(text):
    print("Daisy:", text)
    engine.say(text)
    engine.runAndWait()

# Listen function
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command.lower()
        except:
            speak("Sorry, I didn't catch that.")
            return ""

# Greet based on time
def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Daisy. How can I assist you?")

# Google search
def google_search(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)
    speak(f"Here's what I found for {query} on Google.")

# Open website
def open_website(site):
    site = site.replace(" ", "")  # remove spaces

    # If user says something like "YouTube" or "Instagram", make a safe assumption
    common_sites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "instagram": "https://www.instagram.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://www.twitter.com",
        "linkedin": "https://www.linkedin.com",
        "gmail": "https://mail.google.com"
    }

    if site in common_sites:
        webbrowser.open(common_sites[site])
        speak(f"Opening {site}")
    else:
        if not site.startswith("http"):
            site = f"https://{site}.com"  # assume it's a .com if no domain
        webbrowser.open(site)
        speak(f"Opening {site}")

# Close tab
def close_tab():
    try:
        pyautogui.hotkey('ctrl', 'w')
        speak("Closed the current tab.")
    except Exception as e:
        speak("I couldn't close the tab.")

# Take screenshot with timestamp
def take_screenshot():
    os.makedirs("data", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot = pyautogui.screenshot()
    screenshot.save(f"data/screenshot_{timestamp}.png")
    speak("Screenshot taken and saved in the data folder.")

# Tell joke
def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

# Tell date and time
def tell_date_and_time():
    now = datetime.datetime.now()
    date = now.strftime("%A, %B %d, %Y")
    time = now.strftime("%I:%M %p")
    speak(f"Today is {date} and the time is {time}")

# Take note with better format
def take_note():
    os.makedirs("data", exist_ok=True)
    speak("What would you like me to note?")
    note = listen()
    if note:
        with open("data/notes.txt", "a") as f:
            f.write(f"{datetime.datetime.now()}:\n{note}\n\n")
        speak("Note saved in the data folder.")
    else:
        speak("Nothing noted.")

# Main program loop
def main():
    greet()
    while True:
        command = listen()

        if not command:
            continue

        if "search" in command:
            query = command.replace("search", "").strip()
            if query:
                google_search(query)
            else:
                speak("What should I search for?")

        elif "open" in command:
            site = command.replace("open", "").strip()
            open_website(site)

        elif "close tab" in command or "close this" in command:
            close_tab()

        elif "screenshot" in command:
            take_screenshot()

        elif "joke" in command:
            tell_joke()

        elif "date" in command or "time" in command:
            tell_date_and_time()

        elif "note" in command or "write this" in command:
            take_note()

        elif "exit" in command or "quit" in command or "stop" in command:
            speak("Goodbye!")
            break

        else:
            speak("Sorry, I didn't understand that. Try again.")

# Run Daisy
if __name__ == "__main__":
    main()
