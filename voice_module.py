import speech_recognition as sr
from gtts import gTTS
import os
import streamlit as st
import base64

def listen_from_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Please speak.")
        audio = recognizer.listen(source)
    try:
        st.success("✅ Audio received. Processing...")
        query = recognizer.recognize_google(audio)
        return query
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError:
        return "Sorry, my speech service is down."

def convert_text_to_audio(text, filename="response.mp3"):
    tts = gTTS(text)
    tts.save(filename)
    return filename

def play_audio(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    st.audio(f"data:audio/mp3;base64,{b64}", format="audio/mp3")
