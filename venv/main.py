from cgitb import text
from operator import le
from re import I
from numpy import empty
from speechtotext import *
from flask import Flask 
import pyttsx3
import apiai as sr
import speech_recognition as sr

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)


converter = pyttsx3.init()
# Can be more than 100
converter.setProperty('rate', 175)
# Set volume 0-1
converter.setProperty('volume', 0.5)

r = sr.Recognizer()
r.energy_threshold = 300



currMadlib = ["Once upon a blank, in a kingdom far, far away ", ", there lived a blank princess. ",
"Princess blank was loved by everyone ", "in the kingdom of blank-shire, ", "whether they were members of the royal blank, ", "Knights of the blank Table, ",
"or blank vendors in the town square. ", "Even the blank farmers who lived ","far outisde the tall castle blank adored her!"]
newMadlib = []
wordtype = [". can you say a noun please", " please say an adjective to discribe the princess",
 ". say a silly word, needs to be a noun", ". say an animal", ". Mention a place, a noun of course", ". give me a descriptive adjective please",
  ". give a noun for what the vendors are selling", ". mention a food the farmers are growing", ". give a plural noun"]
wordMatch = ['n', 'a', 'n', 'n', 'n', 'a', 'n', 'n', 'n']
wordAlt = ['n', 's','n','n','n', 's', 'n', 'n', 'n']

@app.route('/')

def main():
    gameOn = True
    wrongRead = True
    converter.say("Hello, what is your name?")
    print("Hello, what is your name?")
    converter.runAndWait()
    #data
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
    userName = name
    converter.say("Hello "+ name+" Welcome to Madlibs, a game where you can add your own words to finish the story")
    print("Hello "+ name+" Welcome to Madlibs, a game where you can add your own words to finish the story")
    converter.say("While I dictate the story to you, I will add blanks in each section of the sentence for you to replace, then i will give you 3 seconds to fill the word")
    print("While I dictate the story to you, I will add blanks in each section of the sentence for you to replace, then i will give you 3 seconds to fill the word")
    converter.say("I'll also tell you what type of word i need, whether it's a noun, verb, or adjective. Do you understand? Say yes or help to continue.")
    print("I'll also tell you what type of word i need, whether it's a noun, verb, or adjective. Do you understand? Say yes or help to continue.")
    converter.runAndWait()
    wrongRead = True
    while wrongRead:
        print("You may speak now......")
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, .25)
            audio = r.listen(source)
        try:
            name = r.recognize_google(audio)
            wrongRead = False
        except:
            print("Could Not Recognize what you said, try again")
            converter.say("Could Not Recognize what you said, try again")
            converter.runAndWait()

    if name == "Yes." or name == 'yes.':
        converter.say("Great, let us begin")
        print("Great, let us begin")
    elif name == "Help." or name == "help.":
        converter.say(helpPage())
        print(helpPage())
    converter.runAndWait()
    #While loop runs on bool gameOn, will handle entire reading and analyzing of story
    index = 0
    while(gameOn):
        if(len(currMadlib) == index):
            gameOn = False
            tobeValidated = False
            
            story = ""
            for a in newMadlib:        
                story += a
            converter.say("You have reached the end of this passage, lets read your story and export")
            print("You have reached the end of this passage, lets read your story and export")
            converter.say(story)
            print(story)
            turnArrToPDF(newMadlib) 
            converter.say("Your story has been exported to a pdf, closing down the application")
            print("Your story has been exported to a pdf, closing down the application")
            converter.runAndWait()
            os.close()

    
        converter.say(currMadlib[index] + wordtype[index])
        print(currMadlib[index] + wordtype[index])
        converter.runAndWait()
        tobeValidated = True

        #While loop checks if a word needs to be validated, will handle error checking
        while (tobeValidated):
            wrongRead = True
            while wrongRead:
                print("You may speak now......")
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, .25)
                    audio = r.listen(source)
                try:
                    name = r.recognize_google(audio)
                    wrongRead = False
                except:
                    print("Could Not Recognize what you said, try again")
                    converter.say("Could Not Recognize what you said, try again")
                    converter.runAndWait()
                    break
            if wrongRead:
                continue
                    

            if word_count(name) == 1: #checks if only one word was stated
                check = name.lower()
                check = check.replace('.', '')
                if(check == "help"):
                    converter.say(helpPage())
                    print(helpPage())
                    converter.runAndWait()
                    break
                
                print("word is: "+check)
                set = wordAnalyzer(check)
                print(set)
                if (wordMatch[index] in set or wordAlt[index] in set): #checks if word matches neccessary requirements, appends index
                    newMadlib.append(currMadlib[index])
                    newMadlib[index] = newMadlib[index].replace("blank", check)
                    index +=1
                    tobeValidated = False
                elif(len(set) == 0):
                    converter.say(wordtype[index])
                    print(wordtype[index])
                    converter.runAndWait()
                else:
                    converter.say("Sorry, that word wont work, say another one")
                    print("Sorry, that word wont work, say another one")
                    converter.say(wordtype[index])
                    print(wordtype[index])
                    converter.runAndWait()

                
            elif word_count(name) == 2: #handles commands "Read Story" and "Finish Story"
                command = name.lower()
                command = command.replace('.', '')
                if('read' in command and 'story' in command): # read story command
                    story = ""
                    for a in newMadlib:
                        
                        story += a
                    converter.say(story)
                    print(story)
                    converter.say("I will now continue dictating the story from the next line")
                    print("I will now continue dictating the story from the next line")
                    converter.runAndWait()
                    tobeValidated = False
                if('finish' in command and 'story' in command): # finish story command
                    turnArrToPDF(newMadlib)
                    converter.say("Story has been exported. I enjoyed your creativity "+ userName+ ", I am now shutting off goodbye.")
                    print("Story has been exported. I enjoyed your creativity "+ userName+ ", I am now shutting off goodbye.")
                    converter.runAndWait()
                    gameOn = False
                    tobeValidated = False
            else:
                converter.say("I didn't understand what you just said, please keep phrases to one or two words until my creators improve my processing power."+
                 "Respond help to review the commands after I read the next line. I will now repeat the last mentioned line.")
                converter.say(wordtype[index])
                print("I didn't understand what you just said, please keep phrases to one or two words until my creators improve my processing power."+
                 "Respond help to review the commands after I read the next line. I will now repeat the last mentioned line.")
                print(wordtype[index])
                converter.runAndWait()