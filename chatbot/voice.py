import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()
engine = pyttsx3.init()


def listen_voice():

    with sr.Microphone() as source:

        print("Listening...")

        audio = recognizer.listen(source)

        text = recognizer.recognize_google(audio)

        return text


def speak(text):

    engine.say(text)
    engine.runAndWait()