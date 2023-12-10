from client import CluelessClient
import tkinter as tk
from tkinter import *
import datetime
import threading
from messaging.message import Message
from Inventory.character import Character
from Inventory.inventory import Inventory
from infoBoard import InfoBoard
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
                inventoryList = client.inventory.getItems()
        except:
            pass
    
def moveMessage():
    contents = {}
    contents["direction"] = inputValMove.get()
    contents["currentLocation"] = client.boardLocation
    printLine = f"Player {original_character_name} requests move {contents['direction']} from {contents['currentLocation']}"
    consoleOutput(printLine)
    move_message = Message("move", original_character_name, contents)
    client.send_message(move_message)
    
def suggesstionMessage():
    contents = {}
    suggestion_suspect = inputValSuggesstionCharacter.get().title()
    contents["suspect"] = suggestion_suspect

    suggestion_weapon = inputValSuggesstionWeapon.get().lower()
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
        accusation_suspect = accusationInputCharacter.get().title()
        contents["suspect"] = accusation_suspect

        accusation_room = accusationInputRoom.get().title()
        contents["room"] = accusation_room 

        accusation_weapon = accusationInputWeapon.get().replace(" ", "").lower()
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
    
    while True:
        print(f"Select from the following characters: {client.availableCharacters}")
        original_character_name = input("Please enter your character name: ")
        #original_character_name = original_character_name.title()
        
        if original_character_name in client.availableCharacters:
            client.character.name = original_character_name
            client.playerName = original_character_name
            break
        else:
            print("Invalid Character Name, Please Select Again")

    #Send character init message
    contents = {}
    contents["characterName"] = client.character.name
    contents["startingLocation"] = client.boardLocation

    init_message = Message("character_init", original_character_name, contents)
    
    client.send_message(init_message)
    
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
    root.title("Clue-Less Application")
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
    inventoryList =['lead pipe', 'revolver', 'weapon2']
    inventoryLabel = Label(root, text="Your Inventory")
    inventoryLabel.config(font=("Courier", 15))
    inventoryLabel.grid(row = 2, column=0, sticky='', columnspan = 1)
    value = 3
    if inventoryList != None:
        for i in inventoryList:
            Label(root, text = "● "+i).grid(row = value, column=0, pady=2)
            value = value + 1
    else: 
        inventoryList = []
        Label(root, text = "awaiting inventory").grid(row = 3, column=0, pady=2)

    #Display Checklist of all possible items
    RoomItems = ['Study', 'Hall','Lounge','Dining Room', 'Kitchen','Ballroom','Conservatory', 'Library', 'Billard Room']
    characterItems = ['Miss Scarlet','Colonel Mustard', 'Missus White','Mister Green', 'Missus Peacock', 'Professor Plum'] 
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
    inputValMove.set("chose a direction")

    # sets up entry message
    directions = ['up', 'down', 'left', 'right', 'secretpassage']
    UserInput = OptionMenu(root, inputValMove, *directions).grid(column=0, row=17, columnspan=5)
    movebutton = Button(root, text="Make a Move", command=moveMessage).grid(column=4, row=17, columnspan=5)

    # suggesstion
    inputValSuggesstionCharacter = StringVar()
    inputValSuggesstionCharacter.set("character option")
    inputValSuggesstionWeapon = StringVar()
    inputValSuggesstionWeapon.set("weapon option")
    userInputCharacterSuggest = OptionMenu(root, inputValSuggesstionCharacter, *characterItems).grid(column=1, row=18, columnspan=1)
    UserInputSuggestWeapon = OptionMenu(root, inputValSuggesstionWeapon, *weaponItems).grid(column=2, row=18, columnspan=2)
    suggestButton = Button(root, text="Make a Suggestion", command=suggesstionMessage).grid(column=4, row=18, columnspan=5)
    
    #Disprove Set Up 
    disproveInput = StringVar()
    disproveInput.set("item to disprove")
    inventoryListNoOption = inventoryList
    inventoryListNoOption.append("can't disprove suggesstion")
    UserInputDisprove = OptionMenu(root, disproveInput, *inventoryListNoOption).grid(column=0, row=19, columnspan=5)
    disproveButton = Button(root, text="Disprove", command=disproveMessage).grid(column=4, row=19, columnspan=5)
    
    #Accusation Set Up 
    accusationInputCharacter = StringVar()
    accusationInputCharacter.set("Character choice")
    accusationInputWeapon = StringVar()
    accusationInputWeapon.set("Weapon choice")
    accusationInputRoom = StringVar()
    accusationInputRoom.set("Room Choice")
    UserInputAccusationCharacter = OptionMenu(root, accusationInputCharacter, *characterItems).grid(column=1, row=20, columnspan=1)
    UserInputAccusationWeapon = OptionMenu(root, accusationInputWeapon, *weaponItems).grid(column=2, row=20, columnspan=1)
    UserInputAccusationRoom = OptionMenu(root, accusationInputRoom, *RoomItems).grid(column=3, row=20, columnspan=1)
    accusationButton = Button(root, text="Make Accusation", command=accusationMessage).grid(column=4, row=20, columnspan=5)
    
    #Start thread to listen for messages from server
    data_thread = threading.Thread(target=checkServer, args=(client,))
    data_thread.start()
    
    root.mainloop()