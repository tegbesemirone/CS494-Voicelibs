import sys

from cgitb import text
from operator import le
from re import I
from numpy import empty
from util import *
from dialogflow import *
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
        converter = pyttsx3.init()
        

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

  
        self.setGeometry(1000, 500, 2000, 1000)
        
        self.label = QLabel("THIS IS THE START OF THE GAME", self)
        self.label.setGeometry(500, 1000, 300, 300)
        self.label.setWordWrap(True)

        pagelayout.addWidget(self.label)

        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)
        
        self.label.setAlignment(Qt.AlignCenter)

    def textToAudio(transcript):
            converter = pyttsx3.init()
            converter.setProperty('rate', 200)
            converter.setProperty('volume', 0.5)
            converter.say(transcript)
            print(transcript)


    def activate_tab_1(self):
        """
        converter = pyttsx3.init()
        
        #textToAudio("Hello, what is your name?", converter)
        #converter.setProperty('rate', 200)
        #converter.setProperty('volume', 0.5)
        #converter.say("Hello, what is your name?")
        print("Hello, what is your name?")
        #converter.runAndWait()
        name = transcribeAudio()
        self.label.setText(name)
        """
        gameOn = True
        agentResponse = ""
        self.label.setText("Hello, what is your name?")
        QApplication.processEvents()
        textToAudio("Hello, what is your name?")
        name = transcribeAudio()
        userName = callAgent(name)
        self.label.setText("Hello, "+userName+". Welcome to Voice-Libs")
        QApplication.processEvents()
        introAudio(userName)
        name = transcribeAudio()
        agentResponse = callAgent(name)

        #checks if the commands match the accepted phrases, game starts regardless of if the phrases match
        if agentResponse == "Yes":
            self.label.setText("Great let us begin")
            QApplication.processEvents()
            textToAudio("Great, let us begin")
        elif agentResponse == "Help":
            helpPage()

        # While loop runs on bool gameOn, will handle entire reading and analyzing of story
        index = 0
        while (gameOn):
            if (len(currMadlib) == index):
                gameOn = False
                tobeValidated = False
                textToAudio("You have reached the end of this passage, lets read your story and export")
                readStory(newMadlib)
                turnArrToPDF(newMadlib)
                textToAudio("Your story has been exported to a pdf, closing down the application")
                os.close()

            #reads the current line of the story, then reads the wordtype prompt to user.
            textToAudio(currMadlib[index] + wordtype[index])
            tobeValidated = True

            # While loop checks if a word needs to be validated, will handle error checking
            while (tobeValidated):
                name = transcribeAudio()
                agentResponse = callAgent(name)
                print("Agent response: "+agentResponse) #error checking
                if(agentResponse == ""):
                    agentResponse = name
                # checks if only one word was stated
                if word_count(agentResponse) == 1: 

                    #since wordnet only accepts lowercase format, a universal catch-all is implemented 
                    check = agentResponse.lower()
                    check = check.replace('.', '')

                    if(check == "quit"):
                        textToAudio("Turning off now, goodbye "+userName)
                        gameOn = False
                        tobeValidated = False
                        break

                    if(check == "repeat"):
                        textToAudio("Sure, repeating the last line now")
                        break

                    if (check == "help"):
                        helpPage()
                        break
                    print("word is: " + check) #error checking
                    set = wordAnalyzer(check)
                    print(set)
                    # checks if word matches neccessary requirements, appends index
                    if (wordMatch[index] in set or wordAlt[index] in set):  
                        newMadlib.append(currMadlib[index])
                        newMadlib[index] = newMadlib[index].replace("blank", check)
                        index += 1
                        tobeValidated = False

                    elif (len(set) == 0):
                        textToAudio(wordtype[index])

                    else:
                        textToAudio("Sorry, that word wont work, say another one")
                        textToAudio(wordtype[index])
                # handles commands "Read Story" and "Finish Story"
                elif word_count(agentResponse) == 2:  

                    # read story command
                    if (agentResponse == "Read Story"):  
                        readStory(newMadlib)
                        textToAudio("Let's continue from the current line.")
                        tobeValidated = False
                    # finish story command
                    if (agentResponse == "Finish Story"): 
                        turnArrToPDF(newMadlib)
                        textToAudio("Story has been exported. I enjoyed your creativity " + userName + ". Let's listen to your final story, and export it to a pdf to read later!")
                        readStory(newMadlib)
                        gameOn = False
                        tobeValidated = False
                #if nothing can be recognized, reprompt user and explain phrase was not recognized
                else:
                    textToAudio("I didn't understand what you just said, can you rephrase that, or give me another word?")
                    #textToAudio(wordtype[index])
       
        

        

    def activate_tab_2(self):
        self.label.setText("you can press the microphone icon to say the following commands: use FINISH STORY to export the final story to a pdf, use READ STORY to hear your story, use HELP to see these commands again")



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()