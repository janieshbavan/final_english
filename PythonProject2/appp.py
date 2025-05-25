import speech_recognition as sr
import requests
from gtts import gTTS
import pygame
import time
import os

RASA_ENDPOINT = "http://localhost:5005/webhooks/rest/webhook"

def listen_from_mic():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("🎤 Please speak...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio, language='en-US')
        print(f"👤 You said: {user_input}")
        return user_input
    except sr.UnknownValueError:
        print("🤖 Sorry, I could not understand what you said.")
        return None
    except sr.RequestError as e:
        print("⚠️ Could not request results from Google Speech Recognition service:", e)
        return None

def send_to_rasa(text):
    payload = {"sender": "user", "message": text}
    try:
        response = requests.post(RASA_ENDPOINT, json=payload)
        if response.ok and response.json():
            return response.json()[0]['text']
        else:
            return "Sorry, I could not get a response."
    except requests.exceptions.RequestException:
        return "Unable to reach Rasa server."

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("response.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.music.stop()
    pygame.mixer.quit()

    if os.path.exists("response.mp3"):
        os.remove("response.mp3")

def main():
    print("📞 Naveen from Tellestia is ready!")
    speak("Hi! This is Naveen from Tellestia. Can I talk to you for a couple of minutes about your business setup?")

    while True:
        input("▶️ Press Enter to start speaking...")

        user_input = listen_from_mic()
        if user_input:
            if any(stop_word in user_input.lower() for stop_word in ["stop", "exit", "quit", "bye"]):
                speak("Thank you! Talk to you soon.")
                break

            rasa_reply = send_to_rasa(user_input)
            print(f"🤖 Reply: {rasa_reply}")
            speak(rasa_reply)
        else:
            speak("Please try speaking again.")

if __name__ == "__main__":
    main()