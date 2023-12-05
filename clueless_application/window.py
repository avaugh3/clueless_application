import client
import tkinter as tk
from tkinter import *
import datetime
#following geeks for geeks tutorial 
# root window
root = tk.Tk()
root.title("Clue-Less Application")
root.geometry("750x750")

# set title
title = Label(root, text="Clue-Less Info Board")                        
title.grid(row=0, column=0, sticky='', columnspan = 5)
title.config(font=("Courier", 34))

# display character Info
#TODO it's with the get name function but that is just hard coded
characterInformation = 'Character Information: ' + client.Character.getName(client.Character)
characterdisplay = Label(root, text=characterInformation)
characterdisplay.grid(row = 1, column=0, sticky='', columnspan = 5)
characterdisplay.config(font=("Courier", 25))

#Display Characters inventory
#TODO get the inventory lists function to display right
inventoryList = client.Inventory.getItems(client.Inventory)
inventoryLabel = Label(root, text="Your Inventory")
inventoryLabel.config(font=("Courier", 15))
inventoryLabel.grid(row = 2, column=0, sticky='', columnspan = 1)
value = 3
for i in inventoryList:
    Label(root, text = "● "+i).grid(row = value, column=0, pady=2)
    value = value + 1


#Display Checklist of all possible items
RoomItems = ['Study', 'Hall','Lounge','Dining Room', 'Kitchen','Ballroom','Conservatory', 'Library']
characterItems = ['Miss Scarlet','Col. Mustard', 'Mrs. White','Mr. Green', 'Mrs. Peacock', 'Prof. Plum'] 
weaponItems = ['Rope', 'Lead Pipe', 'Knife', 'Wrench', 'Candlestick', 'Revolver']
checklist = Label(root, text="Item Checklists")
checklist.config(font=("Courier", 15))
checklist.grid(row = 2, column=2, sticky='', columnspan = 3)
line = 3
for x in RoomItems:
    Checkbutton(root, text=x).grid(row = line, column=2, sticky='W')
    line = line + 1
line = 3
for x in characterItems:
    Checkbutton(root, text=x).grid(row = line, column=3, sticky='W')
    line = line + 1
line = 3
for x in weaponItems:
    Checkbutton(root, text=x).grid(row = line, column=4, sticky='W')
    line = line + 1

# Display Broadcast of messagess
gameOutputTitle = Label(root, text="\nOutput From Game")
gameOutputTitle.config(font=("Courier", 15))
gameOutputTitle.grid(row = 11, column=1, sticky='', columnspan = 3, pady=2)
# sets up the frame for the text entry
mainframe = Frame(root)
mainframe.grid(column=0, row=13, columnspan=5)
outputtext = Text(mainframe, width=80, height=10)
outputtext.grid(column=1, row=14, columnspan=5)

#TODO this needs to be called by the client item
def consoleOutput(message):
    outputtext.insert(END, message + '\n')

# just some test data
consoleOutput("this is a test output")
consoleOutput("SECOND TEst out")

#Set up user input
gameInputTitle = Label(root, text="\nInput From Game")
gameInputTitle.config(font=("Courier", 15))
gameInputTitle.grid(row = 15, column=1, sticky='', columnspan = 3, pady=2)
# prints out instructions
InstructionsLabel = Label(root, text="For move type: move, direction \n for accusation type: accusation, characterName, roomName, weaponName \n for disprove type: disprove, itemName \n for suggesstion type: suggest, character, weapon")
InstructionsLabel.grid(column = 1, row = 16, columnspan=3)
inputVal = StringVar()
# sets up entry message
UserInput = Entry(root, textvariable=inputVal, font=("arial", 15), width=50).grid(column=0, row=17, columnspan=5)
def sendInput():
    # this would call sendMessage function
    consoleOutput(inputVal.get())
    client.send_message(client, inputVal.get())
button1 = Button(root, text="Enter", command=sendInput).grid(column=4, row=17, columnspan=5)
root.mainloop()