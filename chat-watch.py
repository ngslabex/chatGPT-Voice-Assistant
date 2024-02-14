import os
import openai
from dotenv import load_dotenv
import time
import speech_recognition as sr
import pyttsx3
import numpy as np
from gtts import gTTS

mytext = 'Hosgeldiniz'
language = 'tr'
# from os.path import join, dirname
# import matplotlib.pyplot as plt
# ^ matplotlib is great for visualising data and for testing purposes but usually not needed for production
openai.api_key=''
load_dotenv()
model = 'gpt-3.5-turbo'
model = 'gpt-4'
# Set up the speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init("dummy")
voice = engine.getProperty('voices')[1]
engine.setProperty('voice', voice.id)
name = "Emiralp"
greetings = [f"Merhaba {name}",
             "Nasilsin?",
             "Ben Chat Watch. Bugün iyisin umarım, keyifler yerinde mi?"]
def listen_for_wake_word(source):
    print("Dinliyorum 'Hey'...")

    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if "hey" in text.lower():
                print("Wake word detected.")
                engine.say(np.random.choice(greetings))
                engine.runAndWait()
                listen_and_respond(source)
                break
        except sr.UnknownValueError:
            pass
# Listen for input and respond with OpenAI API
def listen_and_respond(source):
    print("Dinliyorum...")
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"Bunu soyledin: {text}")
            if not text:
                continue
            # Send input to OpenAI API
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{text}"}])
            response_text = response.choices[0].message.content
            print(response_text)
            print("generating audio")
            myobj = gTTS(text = response_text, lang = language, slow = False)
            myobj.save("cevap.mp3")
            print("speaking")
            os.system("vlc cevap.mp3")
            # Speak the response
            print("speaking")
            engine.say(response_text)
            engine.runAndWait()
            if not audio:
                listen_for_wake_word(source)
        except sr.UnknownValueError:
            time.sleep(2)
            print("Kimse konusmuyor, uykuya daliyorum...")
            listen_for_wake_word(source)
            break
        except sr.RequestError as e:
            print(f"Istek bulunamadi; {e}")
            engine.say(f"Istek bulunamadi; {e}")
            engine.runAndWait()
            listen_for_wake_word(source)
            break

# Use the default microphone as the audio source
with sr.Microphone() as source:
    listen_for_wake_word(source)
