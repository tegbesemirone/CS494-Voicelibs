from cgitb import text
from operator import le
from re import I
from numpy import empty
from speechtotext import *
from flask import * 
import pyttsx3
import apiai as sr
import speech_recognition as sr
import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel

converter = pyttsx3.init()
# Can be more than 100
converter.setProperty('rate', 175)
# Set volume 0-1
converter.setProperty('volume', 0.5)

r = sr.Recognizer()
r.energy_threshold = 300
r.dynamic_energy_threshold = True

#array with the Madlib story
currMadlib = ["Once upon a blank, in a kingdom far, far away ", ", there lived a blank princess. ",
              "Princess blank was loved by everyone ", "in the kingdom of blank-shire, ",
              "whether they were members of the royal blank, ", "Knights of the blank Table, ",
              "or blank vendors in the town square. ", "Even the blank farmers who lived ",
                    "far outisde the tall castle blank adored her!", "or blank vendors in the town square. ", "Even the blank farmers who lived ","far outisde the tall castle blank adored her!",
        "The gentle princess had a blank childhood", " blanking in the garden, playing music", "on her blank-string harp",
        "and learning to blank-fight with her father",", the brave King blank the third.", "But one night, something blank happened that changed her life forever.",
        "A blank-breathing dragon", " with two blanks attacked the castle!", "The king suddenly blanks after defending the castle and was never heard from again" ]
newMadlib = []
#array with word prompts
wordtype = [". can you say a noun please", " please say an adjective to describe the princess",
            ". say a silly word, needs to be a noun", ". say an animal", ". Mention a place, a noun of course",
            ". give me a descriptive adjective please",
            ". give a noun for what the vendors are selling", ". mention a food the farmers are growing",
            ". give a plural noun", ". give a noun for what the vendors are selling", ". mention a food the farmers are growing", ". give a plural noun", ". please provide an adjective", "Provide a verb, ill add -ing to it",
  ".give me a number please", ". say a noun, any noun", "give me a noun, i may not recognize all pronouns", "I'm looking for an adjective here", ". give me a noun, any noun", "say a body part, but make sure to say the singular version, ill make it plural",
  "say a verb please"]
wordMatch = ['n', 'a', 'n', 'n', 'n', 'a', 'n', 'n', 'n', 'a', 'v', 'n', 'n', 'n', 'a', 'n','n', 'v']
wordAlt = ['n', 's','n','n','n', 's', 'n', 'n', 'n', 's','v','n', 's', 'n', 's', 'n','n', 's']



# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("VoiceLibs")

        button = QPushButton("Press Me to Create your Own Story!", self)
        button.setGeometry(200, 150, 100, 40)
        button.clicked.connect(self.start)

        self.setFixedSize(QSize(400, 300))

        # Set the central widget of the Window.
        self.setCentralWidget(button)
        #self.setCentralWidget(widget)
        self.show()



    def start(self):
        self.button.hide()
        gameOn = True
        wrongRead = True
        converter.say("Hello, what is your name?")


        widget = QLabel("Hello, what is your name?")
        font = widget.font()
        font.setPointSize(30)
        widget.setFont(font)
        widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        converter.runAndWait()
        audio = 0
        while wrongRead:
            print("You may speak now......")
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, .25)
                audio = r.listen(source)
            #name = transcribeAudio(data, "output.wav")
            try:
                name = r.recognize_google(audio)
                wrongRead = False
            except:
                print("Could Not Recognize what you said, try again")
                converter.say("Could Not Recognize what you said, try again")
                converter.runAndWait()



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()