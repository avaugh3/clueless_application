import client
import tkinter as tk
from tkinter import *
import datetime
#following geeks for geeks tutorial 
# root window
root = tk.Tk()
root.title("Clue-Less Application")
root.geometry("750x750")
#frame = Frame(root)
#frame.pack()
# set title
title = Label(root, text="Clue-Less Application")                        
title.grid(row=0, column=0, sticky='', columnspan = 5)
title.config(font=("Courier", 34))

# display character Info
#TODO it's with the get name function but that is just hard coded
characterInformation = 'Character Information: ' + client.Character.getName(client.Character)
characterdisplay = Label(root, text=characterInformation)
characterdisplay.grid(row = 1, column=0, sticky='', columnspan = 5)
characterdisplay.config(font=("Courier", 25))

#Display Characters inventory 
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

# display output of console 
# think this needs to get called by the client
mainframe = Frame(root)
mainframe.grid(column=0, row=11, columnspan=5)
outputtext = Text(mainframe)
outputtext.grid(column=1, row=12, columnspan=5)

def consoleOutput(message):
    outputtext.insert(END, message + '\n')
consoleOutput("this is a test output")
consoleOutput("SECOND TEst out")



root.mainloop()