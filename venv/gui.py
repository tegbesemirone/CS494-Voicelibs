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
currMadlib = ["Once upon a blank, in a kingdom far, far away. ", 
", there lived a blank princess. ",
"Princess blank was loved by everyone. ", 
"in the kingdom of blank-shire, ",
"whether they were members of the royal blank, ", 
"Knights of the blank Table, ",
"or blank vendors in the town square. ", 
"Even the blank farmers who lived. ",
"far outisde the tall castle blank adored her! ", 
"The gentle princess had a blank childhood. ", 
"blanking in the garden, playing music. ", 
"on her blank-string harp ",
"and learning to blank-fight with her father, ",
"the brave King blank the third. ", 
"But one night, something blank happened that changed her life forever. ",
"A blank-breathing dragon ", 
"with two blanks attacked the castle! ", 
"The king suddenly blanks after defending the castle and was never heard from again." ]
newMadlib = []
#array with word prompts
wordtype = ["Can you say a noun please?", 
" Please say an adjective to describe the princess.",
"Say a silly word, needs to be a noun.", 
"Say an animal", 
"Mention a place, a noun of course.",
"Give me a descriptive adjective please.",
"Give a noun for what the vendors are selling.", 
"Mention a food the farmers are growing.",
"Give a plural noun.", 
"Please provide an adjective.", 
"Provide a verb, I'll add -ing to it.",
"Give me a number please.", 
"Say a noun, any noun.", 
"Give me a noun, I may not recognize all pronouns.",
"I'm looking for an adjective here.", 
"Give me a noun, any noun.", 
"Say a body part, but make sure to say the singular version, I'll make it plural.",
"Say a verb please."]
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

        btn = QPushButton("start")
        btn.pressed.connect(self.activate_tab_1)
        button_layout.addWidget(btn)
        btn.setStyleSheet("background-color : green;font-size: 20pt;")

        btn = QPushButton("help")
        btn.pressed.connect(self.activate_tab_2)
        button_layout.addWidget(btn)
        btn.setStyleSheet("background-color : purple; font-size: 20pt;")

        btn = QPushButton("how to play")
        btn.pressed.connect(self.activate_tab_3)
        button_layout.addWidget(btn)
        btn.setStyleSheet("background-color : blue ;font-size: 20pt;")
        
        self.label = QLabel("Click the green button to start the game!", self)
        self.label.setStyleSheet("color: white; font-size: 60pt;")
        #self.label.setGeometry(100, 60, 1000, 800)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        pagelayout.addWidget(self.label)

        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)
        self.setGeometry(1000, 500, 2000, 1000)

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
        self.label.setText("Hello, "+ userName +". Welcome to Voice-Libs")
        QApplication.processEvents()
        #textToAudio("Hello " + userName + " Welcome to Voice-libs.")
        introAudio()
        name = transcribeAudio()
        agentResponse = callAgent(name)

        #checks if the commands match the accepted phrases, game starts regardless of if the phrases match
        if agentResponse == "Yes":
            self.label.setText("Great let us begin!")
            QApplication.processEvents()
            textToAudio("Great, let us begin")
        elif agentResponse == "Help":
            self.label.setText("Game will begin after help audio. ")
            QApplication.processEvents()
            helpPage()

        # While loop runs on bool gameOn, will handle entire reading and analyzing of story
        index = 0
        while (gameOn):
            if (len(currMadlib) == index):
                gameOn = False
                tobeValidated = False
                self.label.setText("Lets read your story and export")
                QApplication.processEvents()
                textToAudio("You have reached the end of this passage, lets read your story and export")
                QApplication.processEvents()
                readStory(newMadlib)
                turnArrToPDF(newMadlib)
                self.label.setText("Closing the application now...")
                QApplication.processEvents()
                textToAudio("Your story has been exported to a pdf, closing down the application")
                os.close()

            #reads the current line of the story, then reads the wordtype prompt to user.
            self.label.setText(currMadlib[index] + wordtype[index])
            QApplication.processEvents()
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
                        self.label.setText("Goodbye, " +userName)
                        QApplication.processEvents()
                        textToAudio("Turning off now, goodbye "+userName)
                        gameOn = False
                        tobeValidated = False
                        break

                    if(check == "repeat"):
                        self.label.setText("Repeating the last line now.")
                        QApplication.processEvents()
                        textToAudio("Sure, repeating the last line now.")
                        break

                    if (check == "help"):
                        self.label.setText("Help audio now playing. ")
                        QApplication.processEvents()
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
                        QApplication.processEvents()
                        textToAudio(wordtype[index])

                    else:
                        self.label.setText("Say another word!")
                        QApplication.processEvents()
                        textToAudio("Sorry, that word wont work, say another one.")
                        textToAudio(wordtype[index])
                # handles commands "Read Story" and "Finish Story"
                elif word_count(agentResponse) == 2:  

                    # read story command
                    if (agentResponse == "Read Story"):
                        self.label.setText(userName+", your current story is now playing.")  
                        QApplication.processEvents()
                        readStory(newMadlib)
                        self.label.setText(userName+", let's continue making your story!") 
                        QApplication.processEvents()
                        textToAudio("Let's continue from the current line.")
                        tobeValidated = False
                    # finish story command
                    if (agentResponse == "Finish Story"): 
                        turnArrToPDF(newMadlib)
                        QApplication.processEvents()
                        textToAudio("Story has been exported. I enjoyed your creativity, " + userName + ". Let's listen to your final story, and export it to a pdf to read later!")
                        self.label.setText(userName+", your final story is now playing!")
                        QApplication.processEvents()
                        readStory(newMadlib)
                        self.label.setText("The game is now over "+userName+", press start to begin a new session.")
                        QApplication.processEvents()
                        
                        gameOn = False
                        tobeValidated = False
                #if nothing can be recognized, reprompt user and explain phrase was not recognized
                else:
                    textToAudio("I didn't understand what you just said, can you rephrase that, or give me another word?")
                    #textToAudio(wordtype[index])
       

    def activate_tab_2(self):
        #help tab
        self.label.setText("say FINISH STORY to export the final story to a pdf, say READ STORY to hear your story, or say HELP to see hear commands again")
        helpPage()
        QApplication.processEvents()

    def activate_tab_3(self):
        #how-to tab/introduction
        self.label.setText("Welcome to Voice Libs!")
        introAudio()
        QApplication.processEvents()


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()