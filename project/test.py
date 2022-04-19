import speech_recognition as sr 
from gtts import gTTS 
import os 
import time
import playsound
from flask import Blueprint, render_template, url_for, request, session, g

from os import *
def speak(text):
    text="안녕하세요 11조 화이팅입니다."
    tts=gTTS(text=text, lang='ko')
    filename='voice.mp3'
    tts.save(filename)
    return playsound.playsound(filename)

