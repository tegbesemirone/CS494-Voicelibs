from cgitb import text
from operator import le
from re import I
from numpy import empty
from speechtotext import *
from dialogflow import *
from flask import *


# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)



#array with the Madlib story
currMadlib = ["Once upon a blank, in a kingdom far, far away ", ", there lived a blank princess. ",
              "Princess blank was loved by everyone ", "in the kingdom of blank-shire, ",
              "whether they were members of the royal blank, ", "Knights of the blank Table, ",
              "or blank vendors in the town square. ", "Even the blank farmers who lived ",
              "far outisde the tall castle blank adored her!"]
newMadlib = []
#array with word prompts
wordtype = [". can you say a noun please", " please say an adjective to discribe the princess",
            ". say a silly word, needs to be a noun", ". say an animal", ". Mention a place, a noun of course",
            ". give me a descriptive adjective please",
            ". give a noun for what the vendors are selling", ". mention a food the farmers are growing",
            ". give a plural noun"]
wordMatch = ['n', 'a', 'n', 'n', 'n', 'a', 'n', 'n', 'n']
wordAlt = ['n', 's', 'n', 'n', 'n', 's', 'n', 'n', 'n']


@app.route('/')
def main():
    gameOn = True

    #calls the dialoflow agent for better answer response analysis from application
    agentResponse = " "
    textToAudio("Hello, what is your name?")
    name = transcribeAudio()
    userName = callAgent(name)
    textToAudio("Hello " + userName + " Welcome to Madlibs, a game where you can add your own words to finish the story")
    textToAudio(
        "While I dictate the story to you, I will add blanks in each section of the sentence for you to replace, then i will give you 3 seconds to fill the word")
    textToAudio(
        "I'll also tell you what type of word i need, whether it's a noun, verb, or adjective. If you need additional help, just ask for it. Do you understand?")
    name = transcribeAudio()
    agentResponse = callAgent(name)

    #checks if the commands match the accepted phrases, game starts regardless of if the phrases match
    if agentResponse == "Yes":
        textToAudio("Great, let us begin")
    elif agentResponse == "Help":
        textToAudio(helpPage())

    # While loop runs on bool gameOn, will handle entire reading and analyzing of story
    index = 0
    while (gameOn):
        if (len(currMadlib) == index):
            gameOn = False
            tobeValidated = False

            story = ""
            for a in newMadlib:
                story += a
            textToAudio("You have reached the end of this passage, lets read your story and export")
            textToAudio(story)
            turnArrToPDF(newMadlib)
            textToAudio("Your story has been exported to a pdf, closing down the application")
            os.close()

        textToAudio(currMadlib[index] + wordtype[index])
        tobeValidated = True

        # While loop checks if a word needs to be validated, will handle error checking
        while (tobeValidated):

            name = transcribeAudio()


            if word_count(name) == 1:  # checks if only one word was stated

                check = name.lower()
                check = check.replace('.', '')
                if (check == "help"):

                    textToAudio(helpPage())
                    break

                print("word is: " + check)
                set = wordAnalyzer(check)
                print(set)
                if (wordMatch[index] in set or wordAlt[index] in set):  # checks if word matches neccessary requirements, appends index

                    newMadlib.append(currMadlib[index])
                    newMadlib[index] = newMadlib[index].replace("blank", check)
                    index += 1
                    tobeValidated = False
                elif (len(set) == 0):

                    textToAudio(wordtype[index])
                else:
                    textToAudio("Sorry, that word wont work, say another one")
                    textToAudio(wordtype[index])


            elif word_count(name) == 2:  # handles commands "Read Story" and "Finish Story"
                command = name.lower()
                command = command.replace('.', '')
                if ('read' in command and 'story' in command):  # read story command
                    story = ""
                    for a in newMadlib:
                        story += a
                    textToAudio(story)
                    textToAudio("I will now continue dictating the story from the next line")
                    tobeValidated = False
                if ('finish' in command and 'story' in command):  # finish story command
                    turnArrToPDF(newMadlib)
                    textToAudio(
                        "Story has been exported. I enjoyed your creativity " + userName + ", I am now shutting off goodbye.")
                    gameOn = False
                    tobeValidated = False
            else:
                textToAudio(
                    "I didn't understand what you just said, please keep phrases to one or two words until my creators improve my processing power." +
                    "Respond help to review the commands after I read the next line. I will now repeat the last mentioned line.")
                textToAudio(wordtype[index])

if __name__ == '__main__':
    main()