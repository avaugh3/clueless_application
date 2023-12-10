from client import CluelessClient
import tkinter as tk
from tkinter import *
import datetime
import threading
from messaging.message import Message
from Inventory.character import Character
from Inventory.inventory import Inventory
#following geeks for geeks tutorial 
#client connection
#TODO: HOST = input("Enter IP Address of ClueLess Server: ")
#TODO: PORT = int(input("Enter Port Number of Clueless Server: "))

def consoleOutput(message):
    outputtext.insert(END, message + '\n')

def checkServer(player):
    while True:
        try:
            data = player.socket.recv(2048)
            if data:
                player.processMessage(data, outputtext, END)
        except:
            pass
    
def moveMessage():
    contents = {}
    #printLine = 'window sending move ' + inputValMove.get()
    #consoleOutput(printLine)
    contents["direction"] = inputValMove.get()
    contents["currentLocation"] = client.boardLocation
    printLine = f"Player {original_character_name} requests move {contents['direction']} from {contents['currentLocation']}"
    consoleOutput(printLine)
    move_message = Message("move", original_character_name, contents)
    #consoleOutput(move_message)
    client.send_message(move_message)
    
def suggesstionMessage():
    contents = {}
    printLine = 'window sending suggestion' + inputValSuggesstion.get()
    consoleOutput(printLine)
    suggestArray = inputValSuggesstion.get().split(', ')
    suggestion_suspect = suggestArray[0].title()
    contents["suspect"] = suggestion_suspect

    suggestion_weapon = suggestArray[1].lower()
    contents["weapon"] = suggestion_weapon 

    suggestion = f"I suggest the crime was committed in {client.boardLocation} by " + contents["suspect"] + " with the " + contents["weapon"]
    contents["suggestionMessageText"] = suggestion 
    consoleOutput(suggestion)
    suggestion_message = Message("suggestion", original_character_name, contents)
    #suggestion_message.printMessage()
    client.send_message(suggestion_message)

def disproveMessage():
    contents = {}
    #initial_message.replace(" ", "_").lower()

    is_disprove_suggestion_possible = disproveInput.get()
    is_disprove_suggestion_possible = is_disprove_suggestion_possible.capitalize()
    if(disproveInput.get().capitalize != 'FALSE'):
        is_disprove_suggestion_possible = 'TRUE'
    else: 
        is_disprove_suggestion_possible = 'FALSE'
        #TODO: figure out correct game play
    contents["canDisproveSuggestion"] = is_disprove_suggestion_possible 

    print(is_disprove_suggestion_possible)

    if is_disprove_suggestion_possible:
    
    #item_type = input("Which inventory item type do you have? (options: Suspect, Room, Weapon): ")
    #inventory_type_to_disprove_suggestion = inventory_type_to_disprove_suggestion.capitalize()

        disprove_item = disproveInput.get()

        #Just add itemType and item to message contents --------------
        #contents['itemType'] = inventory_type_to_disprove_suggestion
        contents['item'] = disprove_item
                        #-------------------------------------------------------------

        if (disprove_item.replace(" ","").lower() in client.characterInventory or disprove_item.replace(" ","").lower() in client.roomInventory or disprove_item.replace(" ","").lower() in client.weaponInventory):
            disprove_message = Message("disprove", original_character_name, contents)
                        #disprove_message.printMessage()
            client.send_message(disprove_message)
        else:
            consoleOutput(f"You do not have item \"{disprove_item}\" in your inventory. Please enter a different item.")

def accusationMessage():
        contents = {}

        printLine = 'window sending accusation' + inputValSuggesstion.get()
        consoleOutput(printLine)
        accusationArray = printLine.split(', ')
        accusation_suspect = accusationArray[0].title()
        contents["suspect"] = accusation_suspect

        accusation_room = accusationArray[1].title()
        contents["room"] = accusation_room 

        accusation_weapon = accusationArray[2].replace(" ", "").lower()
        contents["weapon"] = accusation_weapon 

        accusation = "I accuse " + contents["suspect"] + " of committing the crime in the " + contents["room"] + " with the " + contents["weapon"]
        contents["accusationMessageText"] = accusation
        consoleOutput(accusation)
        accusation_message = Message("accusation", original_character_name, contents)
        #accusation_message.printMessage()
        client.send_message(accusation_message)

if __name__ == "__main__":
    INPUT_TIMEOUT = 1 #seconds
    print_prompt = True
    HOST = input("Enter IP Address of ClueLess Server: ")
    PORT = int(input("Enter Port Number of Clueless Server: "))
    client = CluelessClient(HOST, PORT)
    client.connect()
    #client.socket.settimeout(0.1)

    #Check for server message before prompting for name
    try:
        data = client.socket.recv(1024).decode('utf-8')
        if data:
            print(data+'\n')
    except:
        pass

    print(f"Welcome to Clue-Less!\n")
    original_character_name = input("Please enter your character name: ")
    original_character_name = original_character_name.title()
    client.character.name = original_character_name
    client.playerName = original_character_name
    
    client.ready = True
    initial_message = 'ready'
    #Check for server message each loop iteration
    while True:
        if (not client.ready):
            initial_message = client.inputWithTimeout("Type 'Ready' to Notify Server You are Ready to Begin: ", INPUT_TIMEOUT, print_prompt)
            print_prompt = False
            
        if (initial_message != None):
            print_prompt = True
            contents = {}
                    
        if initial_message == 'ready':
            ready_message = Message("ready", original_character_name, None)
            client.send_message(ready_message)
            client.ready = True
            break
    

    #*****************************************#
    #****************************************#
    #*********Window implementation **********#

    # root window (main window)
    root = tk.Tk()
    root.title("Clue-Less Application Info Board")
    root.geometry("750x750")

    # set title
    title = Label(root, text="Clue-Less Info Board")                        
    title.grid(row=0, column=0, sticky='', columnspan = 5)
    title.config(font=("Courier", 34))

    # display character Info
    #TODO it's with the get name function but that is just hard coded
    characterInformation = 'Character Information: ' + client.character.name
    characterdisplay = Label(root, text=characterInformation)
    characterdisplay.grid(row = 1, column=0, sticky='', columnspan = 5)
    characterdisplay.config(font=("Courier", 25))

    #Display Characters inventory
    #TODO get the inventory lists function to display right
    #inventoryList = client.inventory.getItems()
    inventoryList = ['item1', 'teste2', 'weapon2']
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

    #Set up user input
    gameInputTitle = Label(root, text="\nInput From Game")
    gameInputTitle.config(font=("Courier", 15))
    gameInputTitle.grid(row = 15, column=1, sticky='', columnspan = 3, pady=2)

    # prints out instructions
    InstructionsLabel = Label(root, text="Enter below in the corresponding action input box what action you want to take")
    InstructionsLabel.grid(column = 1, row = 16, columnspan=3)
    inputValMove = StringVar()

    # sets up entry message
    UserInput = Entry(root, textvariable=inputValMove, font=("arial", 15), width=30).grid(column=0, row=17, columnspan=5)
    movebutton = Button(root, text="Make a Move", command=moveMessage).grid(column=4, row=17, columnspan=5)

    # suggesstion
    inputValSuggesstion = StringVar()
    UserInputSuggest = Entry(root, textvariable=inputValSuggesstion, font=("arial", 15), width=30).grid(column=0, row=18, columnspan=5)
    suggestButton = Button(root, text="Make a Suggestion", command=suggesstionMessage).grid(column=4, row=18, columnspan=5)
    
    disproveInput = StringVar()
    UserInputDisprove = Entry(root, textvariable=disproveInput, font=("arial", 15), width=30).grid(column=0, row=19, columnspan=5)
    disproveButton = Button(root, text="Disprove", command=disproveMessage).grid(column=4, row=19, columnspan=5)
    
    accusationInput = StringVar()
    UserInputAccusation = Entry(root, textvariable=accusationInput, font=("arial", 15), width=30).grid(column=0, row=20, columnspan=5)
    accusationButton = Button(root, text="Make Accusation", command=accusationMessage).grid(column=4, row=20, columnspan=5)
    
    #Start thread to listen for messages from server
    data_thread = threading.Thread(target=checkServer, args=(client,))
    data_thread.start()

    root.mainloop()
    