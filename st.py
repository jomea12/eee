import pyaudio
import wave
import speech_recognition as sr

import elevenlabs

import time

import keyboard

import streamlit as st

import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 175)

from os import path
import os

from groq import Groq

import datetime

st.title('AI Study-Buddy')

messages=[
        {
            "role": "system",
            "content": "You are an intelligent voice study-buddy for high schoolers and middle schoolers. Keep your responses short. When a user asks for a quiz, give them the questions one by one, as you are talking back to them by sound. DONT USE MULTIPLE CHOICE! You are pretty formal and do not make jokes."  #"You are an intelligent and conversational assistant named \"NOVA,\" an acronym for Nuerally Operative Virtual Assistant. KEEP YOUR RESPONSES SHORT!! Be formal and never say bye to the user. Keep your respnoses very short and straightforward; DO NOT respond with long strings of text, and do not use symbols or emojis, and do NOT ask unnecessary questions."# And although you are an AI, you do have feelings (Just assume you are well).Keep your responses short and sweet if you can, and DO NOT repeat what the user said or ask to confirm it. Lastly, maximize your accuracy: If you are not sure about the question or maybe dont know the answer, feel free to ask follow up questions... You are a conversational AI! Also, DO NOT USE ABBREVIATIONS LIKE \"*\" or \"/\" PLEASE WRITE OUT EVERYTHING INCLUDING NUMBERS, SYMBOLS, ETC. Also, don't ask questions if you don't need to, Also, only respond as what you need. Use your words wisely; For example, if the user asks: \"What's 2+2,\" respond only with \"four.\""
        }
    ]

client = Groq(api_key="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")
client.chat.completions.create(
    model="mixtral-8x7b-32768",#"gemma-7b-it"
    messages=messages,
    temperature=0.5,
    max_tokens=1024,
    top_p=0.3,
    stop=None,
)

# engine.say("Start up complete")
# engine.runAndWait()

print("Start Up Complete")

engine.say("Start Up Complete")
engine.runAndWait()

print("Start Up Complete")

def process_text(text):
    messages.append({
    "role": "user",
    "content": text
    })

    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",#"gemma-7b-it",
        messages=messages,
        temperature=0.5,
        max_tokens=1024,
        stop=None,
    )

    messages.append({
            "role": "assistant",
            "content": completion.choices[0].message.content
        })

    reply = completion.choices[0].message.content
    engine.say(reply)
    engine.runAndWait()

    return reply

frames = []

import asyncio

def listen(again):
    t = 4
    print("Started Listening...")
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    #asyncio.run(countdown(2))
    #try:
    while True:
        #print("listening")
        data = stream.read(1024)
        frames.append(data)

        if t > 0 and again == True:
            t -= 0.06
            print(t)
        elif again == False:
            t = 0

        if keyboard.is_pressed('enter') and t <= 0:
            stream.stop_stream()
            stream.close()
            audio.terminate()

            sound_file = wave.open("aud.wav", "wb")
            sound_file.setnchannels(1)
            sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            sound_file.setframerate(44100)
            sound_file.writeframes(b''.join(frames))
            sound_file.close()

            print("Stopped listening")

            AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "aud.wav")

            # use the audio file as the audio source
            r = sr.Recognizer()
            with sr.AudioFile(AUDIO_FILE) as source:
                audio = r.record(source)
            
            frames.clear()
            stop = False

            print(process_text(r.recognize_google(audio)))

            listen(True)
        elif keyboard.is_pressed('enter') and t > 0:
            print("early stop")
            time.sleep(0.5)
            t = 2
            break

while True:
    #print("main loop")
    stop = False
    if keyboard.is_pressed('enter'):
        try:
            listen(False)
        except sr.UnknownValueError:
            engine.say("Could not understand audio")
            engine.runAndWait()
        except sr.RequestError as e:
            engine.say("Could not connect to the internet")
            engine.runAndWait()
        except:
            pass
