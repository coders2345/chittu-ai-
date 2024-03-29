import speech_recognition as sr
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import webbrowser
import os
import datetime
import pyttsx3
import subprocess
import pyautogui
from googlesearch import search
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser
import requests
from bs4 import BeautifulSoup
# Set up Spotify API credentials

# set up speech recognition
r = sr.Recognizer()
mic = sr.Microphone()

# Initialize speech recognizer and engine
engine = pyttsx3.init()

# Define a function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()
# Define a function to execute voice commands
def execute_command(command):
    if "what is your name" in command:
        speak("My name is Chittu. I was developed by Basha.")
    elif "tell about you" in command:
        speak("I am Chittu, a voice assistant developed by Basha.")
    elif "open YouTube" in command:
        webbrowser.open("https://www.youtube.com")
    elif "open Google" in command:
        webbrowser.open("https://www.google.com")
    elif "what time is it" in command:
        now = datetime.datetime.now()
        speak(f"The time is {now.strftime('%H:%M:%S')}")
    elif "play music" in command:
        music_dir = "C:/Users/User/Music"
        songs = os.listdir(music_dir)
        os.startfile(os.path.join(music_dir, songs[0]))
    elif "stop" in command:
        speak("Stopping...")
    elif "open calculator" in command:
        calci= r'C:\Windows\System32\calc.exe'
        subprocess.Popen(calci)
    elif "open edge" in command:
        webbrowser.open("https://www.microsoft.com/en-us/edge")
    elif "open CMD" in command:
        cmd = r'C:\Windows\System32\cmd.exe'
        subprocess.Popen(cmd)
    elif "search" in command:
        speak("what do u want to search")
        with sr.Microphone() as source:
                # Adjust the recognizer for ambient noise
                r.adjust_for_ambient_noise(source)
                # Listen for user input
                audio = r.listen(source, phrase_time_limit=5)
                # Recognize the speech and convert to text
                query = r.recognize_google(audio)
                url = 'https://www.google.com/search?q=' + query
                speak(f"You said: {query} performing google search")
                webbrowser.open(url)

        num_results = 1
        for i, result in enumerate(search(query, num_results=num_results)):
            print(f"Result {i + 1}: {result}")
    elif "spotify" in command:
        speak("which song want to play")
        client_id = 'e727e26f66ce4638ab8bef5cf668506b'
        client_secret = '46c4e8907a3242edbbb02cc4170d819f'
        redirect_uri = 'http://localhost:8000/callback/'
        scope = 'user-modify-playback-state'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri,scope=scope))

        with sr.Microphone() as source:
            # Adjust the recognizer for ambient noise
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, phrase_time_limit=3)
            try:
                text = r.recognize_google(audio)
                print("You said:", text)
            except sr.UnknownValueError:
                speak("Could not understand audio")
            except sr.RequestError as e:
                speak("Could not request results; {0}".format(e))
                results = sp.search(q=text, type='track')
                uri = results['tracks']['items'][0]['uri']
                sp.start_playback(uris=[uri])
# Define the main loop
def check_activation_phrase():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        speak("Say 'basha' to activate me.")
        audio = r.listen(source, phrase_time_limit=3)

    try:
        activation_phrase = r.recognize_google(audio).lower()
        if "basha" in activation_phrase:
            speak("I'm chittu developed by basha what do u want")
            return True
        else:
            speak("Activation phrase not recognized. Please say 'basha' to activate.")
            return False
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand. Please say 'basha' to activate.")
        return False
    except sr.RequestError:
        speak("Sorry, there was an issue with the speech recognition service.")
        return False

# Call the activation function to listen for the activation phrase "basha"
while not check_activation_phrase():
    pass

# Main loop for listening to user commands
chat_mode = False
while True:
    try:
        with sr.Microphone() as source:
            # Adjust the recognizer for ambient noise
            r.adjust_for_ambient_noise(source)
            if not chat_mode:
                speak("Ready for command")
            else:
                speak("Listening for chat input")

            # Listen for user input
            audio = r.listen(source, phrase_time_limit=5)
            # Recognize the speech and convert to text
            command = r.recognize_google(audio).lower()

            # Check if the user says "quit" to end the loop
            if "quit" in command:
                speak("Goodbye!")
                break

            # Check if the user says "basha" to toggle chat mode
            if "basha" in command:
                chat_mode = not chat_mode
                if chat_mode:
                    speak("Chat mode activated. Please say 'basha' again to exit chat mode.")
                else:
                    speak("Chat mode deactivated. How can I help you?")

            # Execute the appropriate command based on the mode
            if chat_mode:
                execute_command(command, chat_mode=True)
            else:
                execute_command(command)

    except sr.UnknownValueError:
        speak("Sorry, I didn't understand. Please try again.")
    except sr.RequestError:
        speak("Sorry, there was an issue with the speech recognition service.")
