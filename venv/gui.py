import sys

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


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtGui import *

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Voice Libs")
        self.setStyleSheet("background-color: #2b323c")


        pagelayout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()

        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(self.stacklayout)

        btn = QPushButton("start")
        btn.pressed.connect(self.activate_tab_1)
        button_layout.addWidget(btn)
        btn.setStyleSheet("background-color : green")
        


        btn = QPushButton("help")
        btn.pressed.connect(self.activate_tab_2)
        button_layout.addWidget(btn)
        btn.setStyleSheet("background-color : purple")

  
        self.setGeometry(0, 0, 400, 300)
        
        self.label = QLabel(":)", self)
        self.label.setGeometry(200, 150, 100, 50)
        self.label.setWordWrap(True)

        pagelayout.addWidget(self.label)

        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)
        
        self.label.setAlignment(Qt.AlignCenter)


    def activate_tab_1(self):
        gameOn = True
        wrongRead = True
        converter.say("Hello, what is your name?")

        self.label.setText("Hello, what is your name?")

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


    def activate_tab_2(self):
        self.label.setText("you can press the microphone icon to say the following commands: use FINISH STORY to export the final story to a pdf, use READ STORY to hear your story, use HELP to see these commands again")



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()