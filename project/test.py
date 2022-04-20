import speech_recognition as sr 
from gtts import gTTS 
import os 
import time
import shutil
import playsound
from flask import Blueprint, render_template, url_for, request, session, g

from os import *
def speak(text):
    tts=gTTS(text=text, lang='ko')
    filename='voice.mp3'
    
    tts.save('project/BeAwriter/static/'+filename)

speak("안녕하세요")