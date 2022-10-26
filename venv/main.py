from cgitb import text
from speechtotext import *

currMadlib = ["Once upon a blank, in a kingdom far, far away ", ", there lived a blank princess. ",
"Princess blank was loved by everyone ", "in the kingdom of blank-shire, ", "whether they were members of the royal blank, ", "Knights of the blank Table, ",
"or blank vendors in the town square. ", "Even the blank farmers who lived ","far outisde the tall castle blank adored her!"]
newMadlib = []
wordtype = [". can you say a noun please", " please say an adjective to discribe the princess",
 ". say a silly word, needs to be a noun", ". say an animal", ". Mention a place, a noun of course", ". give me a descriptive adjective please",
  ". give a noun for what the vendors are selling", ". mention a food the farmers are growing", ". give a plural noun"]
wordMatch = ['n', 'a', 'n', 'n', 'n', 'a', 'n', 'n', 'n']


def main():
    gameOn = True
    textToAudio("Hello, what is your name?")
    data = recordAudio()
    name = transcribeAudio(data, "output.wav")
    textToAudio("Hello "+ name+" Welcome to Madlibs, a game where you can add your own words to finish the story")
    textToAudio("While I dictate the story to you, I will add blanks in each section of the sentence for you to replace, then i will give you 3 seconds to fill the word")
    textToAudio("I'll also tell you what type of word i need, whether it's a noun, verb, or adjective. Do you understand? Say yes or help to continue.")
    data = recordAudio()
    name = transcribeAudio(data, "output.wav")
    if name == "Yes." or name == 'yes.':
        textToAudio("Great, let us begin")
    
    #While loop runs on bool gameOn, will handle entire reading and analyzing of story
    index = 0
    while(gameOn):
        
        textToAudio(currMadlib[index] + wordtype[index])
        
        tobeValidated = True

        #While loop checks if a word needs to be validated, will handle error checking
        while (tobeValidated):
            data = recordAudio()
            name = transcribeAudio(data, "output.wav")

            if word_count(name) == 1: #checks if only one word was stated
                check = name.lower()
                check = check.replace('.', '')
                print("word is: "+check)
                set = wordAnalyzer(check)
                print(set)
                if (wordMatch[index] in set): #checks if word matches neccessary requirements, appends index
                    newMadlib.append(currMadlib[index])
                    newMadlib[index] = newMadlib[index].replace("blank", check)
                    index +=1
                else:
                    textToAudio("Sorry, that word wont work, say another one")

                tobeValidated = False
            elif word_count(name) == 2: #handles commands
                command = name.lower()
                command = command.replace('.', '')
                if('read' in command and 'story' in command): # read story command
                    story = ""
                    for a in newMadlib:
                        
                        story += a
                        textToAudio(story)
                    textToAudio("I will now continue dictating the story from the last line")
                    tobeValidated = False
                if('finish' in command and 'story' in command): # finish story command
                    turnArrToPDF(newMadlib)
                    gameOn = False
                    tobeValidated = False
            else:
                textToAudio("I didn't understand what you just said, please keep phrases to one or 2 words")
            
               





if __name__ == '__main__':
    main()