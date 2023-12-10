from client import CluelessClient
import tkinter as tk
from tkinter import *
import datetime
import threading
from messaging.message import Message
from Inventory.character import Character
from Inventory.inventory import Inventory
#from window import *

class InfoBoard(tk.Frame):
    def consoleOutput(self,message):
        self.outputtext.insert(END, message + '\n')

    def checkServer(self,player):
        while True:
            try:
                data = player.socket.recv(2048)
                if data:
                    player.processMessage(data, self.outputtext, END)
                    inventoryList = self.client.inventory.getItems()
            except:
                pass
        
    def moveMessage(self):
        contents = {}
        contents["direction"] = self.inputValMove.get()
        contents["currentLocation"] = self.client.boardLocation
        printLine = f"Player {self.original_character_name} requests move {contents['direction']} from {contents['currentLocation']}"
        self.consoleOutput(printLine)
        move_message = Message("move", self.original_character_name, contents)
        self.client.send_message(move_message)
        
    def suggesstionMessage(self):
        contents = {}
        suggestion_suspect = self.inputValSuggesstionCharacter.get().title()
        contents["suspect"] = suggestion_suspect

        suggestion_weapon = self.inputValSuggesstionWeapon.get().lower()
        contents["weapon"] = suggestion_weapon 

        suggestion = f"I suggest the crime was committed in {self.client.boardLocation} by " + contents["suspect"] + " with the " + contents["weapon"]
        contents["suggestionMessageText"] = suggestion 
        self.consoleOutput(suggestion)
        suggestion_message = Message("suggestion", self.original_character_name, contents)
        #suggestion_message.printMessage()
        self.client.send_message(suggestion_message)

    def disproveMessage(self):
        contents = {}
        #initial_message.replace(" ", "_").lower()

        is_disprove_suggestion_possible = self.disproveInput.get()
        is_disprove_suggestion_possible = is_disprove_suggestion_possible.capitalize()
        if(self.disproveInput.get().capitalize != 'FALSE'):
            is_disprove_suggestion_possible = 'TRUE'
        else: 
            is_disprove_suggestion_possible = 'FALSE'
            #TODO: figure out correct game play
        contents["canDisproveSuggestion"] = is_disprove_suggestion_possible 

        print(is_disprove_suggestion_possible)

        if is_disprove_suggestion_possible:
        
        #item_type = input("Which inventory item type do you have? (options: Suspect, Room, Weapon): ")
        #inventory_type_to_disprove_suggestion = inventory_type_to_disprove_suggestion.capitalize()

            disprove_item = self.disproveInput.get()

            #Just add itemType and item to message contents --------------
            #contents['itemType'] = inventory_type_to_disprove_suggestion
            contents['item'] = disprove_item
                            #-------------------------------------------------------------

            if (disprove_item.replace(" ","").lower() in self.client.characterInventory or disprove_item.replace(" ","").lower() in self.client.roomInventory or disprove_item.replace(" ","").lower() in self.client.weaponInventory):
                disprove_message = Message("disprove", self.original_character_name, contents)
                            #disprove_message.printMessage()
                self.client.send_message(disprove_message)
            else:
                self.consoleOutput(f"You do not have item \"{disprove_item}\" in your inventory. Please enter a different item.")

    def accusationMessage(self):
            contents = {}
            accusation_suspect = self.accusationInputCharacter.get().title()
            contents["suspect"] = accusation_suspect

            accusation_room = self.accusationInputRoom.get().title()
            contents["room"] = accusation_room 

            accusation_weapon = self.accusationInputWeapon.get().replace(" ", "").lower()
            contents["weapon"] = accusation_weapon 

            accusation = "I accuse " + contents["suspect"] + " of committing the crime in the " + contents["room"] + " with the " + contents["weapon"]
            contents["accusationMessageText"] = accusation
            self.consoleOutput(accusation)
            accusation_message = Message("accusation", self.original_character_name, contents)
            #accusation_message.printMessage()
            self.client.send_message(accusation_message)
    #root = tk.Tk()
    #root.title("Clue-Less Application")
    #root.geometry("750x750")

    def __init__(self, master=None, client=None, **kwargs):
        super().__init__(client, master, **kwargs)
        self.client = client

        # set title
        title = Label(self, text="Clue-Less Info Board")                        
        title.grid(row=0, column=0, sticky='', columnspan = 5)
        title.config(font=("Courier", 34))

        # display character Info
        #TODO it's with the get name function but that is just hard coded
        characterInformation = 'Character Information: ' + self.client.character.name
        characterdisplay = Label(self, text=characterInformation)
        characterdisplay.grid(row = 1, column=0, sticky='', columnspan = 5)
        characterdisplay.config(font=("Courier", 25))

        #Display Characters inventory
        #TODO get the inventory lists function to display right
        #inventoryList = client.inventory.getItems()
        inventoryList =['lead pipe', 'revolver', 'weapon2']
        inventoryLabel = Label(self, text="Your Inventory")
        inventoryLabel.config(font=("Courier", 15))
        inventoryLabel.grid(row = 2, column=0, sticky='', columnspan = 1)
        value = 3
        if inventoryList != None:
            for i in inventoryList:
                Label(self, text = "● "+i).grid(row = value, column=0, pady=2)
                value = value + 1
        else: 
            inventoryList = []
            Label(self, text = "awaiting inventory").grid(row = 3, column=0, pady=2)

        #Display Checklist of all possible items
        RoomItems = ['Study', 'Hall','Lounge','Dining Room', 'Kitchen','Ballroom','Conservatory', 'Library', 'Billard Room']
        characterItems = ['Miss Scarlet','Colonel Mustard', 'Missus White','Mister Green', 'Missus Peacock', 'Professor Plum'] 
        weaponItems = ['Rope', 'Lead Pipe', 'Knife', 'Wrench', 'Candlestick', 'Revolver']
        checklist = Label(self, text="Item Checklists")
        checklist.config(font=("Courier", 15))
        checklist.grid(row = 2, column=2, sticky='', columnspan = 3)
        line = 3
        for x in RoomItems:
            Checkbutton(self, text=x).grid(row = line, column=2, sticky='W')
            line = line + 1
        line = 3
        for x in characterItems:
            Checkbutton(self, text=x).grid(row = line, column=3, sticky='W')
            line = line + 1
        line = 3
        for x in weaponItems:
            Checkbutton(self, text=x).grid(row = line, column=4, sticky='W')
            line = line + 1

        # Display Broadcast of messagess
        gameOutputTitle = Label(self, text="\nOutput From Game")
        gameOutputTitle.config(font=("Courier", 15))
        gameOutputTitle.grid(row = 11, column=1, sticky='', columnspan = 3, pady=2)

        # sets up the frame for the text entry
        mainframe = Frame(self)
        mainframe.grid(column=0, row=13, columnspan=5)
        outputtext = Text(mainframe, width=80, height=10)
        outputtext.grid(column=1, row=14, columnspan=5)

        #Set up user input
        gameInputTitle = Label(self, text="\nInput From Game")
        gameInputTitle.config(font=("Courier", 15))
        gameInputTitle.grid(row = 15, column=1, sticky='', columnspan = 3, pady=2)

        # prints out instructions
        InstructionsLabel = Label(self, text="Enter below in the corresponding action input box what action you want to take")
        InstructionsLabel.grid(column = 1, row = 16, columnspan=3)
        inputValMove = StringVar()
        inputValMove.set("chose a direction")

        # sets up entry message
        directions = ['up', 'down', 'left', 'right', 'secretpassage']
        UserInput = OptionMenu(self, inputValMove, *directions).grid(column=0, row=17, columnspan=5)
        movebutton = Button(self, text="Make a Move", command=self.moveMessage).grid(column=4, row=17, columnspan=5)

        # suggesstion
        inputValSuggesstionCharacter = StringVar()
        inputValSuggesstionCharacter.set("character option")
        inputValSuggesstionWeapon = StringVar()
        inputValSuggesstionWeapon.set("weapon option")
        userInputCharacterSuggest = OptionMenu(self, inputValSuggesstionCharacter, *characterItems).grid(column=1, row=18, columnspan=1)
        UserInputSuggestWeapon = OptionMenu(self, inputValSuggesstionWeapon, *weaponItems).grid(column=2, row=18, columnspan=2)
        suggestButton = Button(self, text="Make a Suggestion", command=self.suggesstionMessage).grid(column=4, row=18, columnspan=5)

        #Disprove Set Up 
        disproveInput = StringVar()
        disproveInput.set("item to disprove")
        inventoryListNoOption = inventoryList
        inventoryListNoOption.append("can't disprove suggesstion")
        UserInputDisprove = OptionMenu(self, disproveInput, *inventoryListNoOption).grid(column=0, row=19, columnspan=5)
        disproveButton = Button(self, text="Disprove", command=self.disproveMessage).grid(column=4, row=19, columnspan=5)

        #Accusation Set Up 
        accusationInputCharacter = StringVar()
        accusationInputCharacter.set("Character choice")
        accusationInputWeapon = StringVar()
        accusationInputWeapon.set("Weapon choice")
        accusationInputRoom = StringVar()
        accusationInputRoom.set("Room Choice")
        UserInputAccusationCharacter = OptionMenu(self, accusationInputCharacter, *characterItems).grid(column=1, row=20, columnspan=1)
        UserInputAccusationWeapon = OptionMenu(self, accusationInputWeapon, *weaponItems).grid(column=2, row=20, columnspan=1)
        UserInputAccusationRoom = OptionMenu(self, accusationInputRoom, *RoomItems).grid(column=3, row=20, columnspan=1)
        accusationButton = Button(self, text="Make Accusation", command=self.accusationMessage).grid(column=4, row=20, columnspan=5)

        #Start thread to listen for messages from server
        data_thread = threading.Thread(target=self.checkServer, args=(client,))
        data_thread.start()
