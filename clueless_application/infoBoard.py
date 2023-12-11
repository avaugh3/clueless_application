import tkinter as tk
from tkinter import *
import threading

class InfoBoard(Frame):
    def __init__(self, master=None, client=None):
        super().__init__(master)
        self.master = master
        self.client = client
        self.pack()
        self.create_widgets()
    
    def consoleOutput(self,message, outputtext):
        outputtext.insert(END, message + '\n')

    def checkServer(self,player, outputtext):
        while True:
            try:
                data = player.socket.recv(2048)
                if data:
                    player.processMessage(data, outputtext, END)
                    inventoryList = self.client.inventory.getItems()
            except:
                pass
        
    def moveMessage(self, inputValMove, outputtext):
        contents = {}
        contents["direction"] = inputValMove.get()
        contents["currentLocation"] = self.client.boardLocation
        printLine = f"Player {self.client.character.name} requests move {contents['direction']} from {contents['currentLocation']}"
        self.consoleOutput(printLine, outputtext)
        move_message = Message("move", self.client.character.name, contents)
        self.client.send_message(move_message)
        
    def suggesstionMessage(self, inputValSuggesstionCharacter,inputValSuggesstionWeapon, outputtext):
        contents = {}
        suggestion_suspect = inputValSuggesstionCharacter.get().title()
        contents["suspect"] = suggestion_suspect

        suggestion_weapon = inputValSuggesstionWeapon.get().lower()
        contents["weapon"] = suggestion_weapon 

        suggestion = f"I suggest the crime was committed in {self.client.boardLocation} by " + contents["suspect"] + " with the " + contents["weapon"]
        contents["suggestionMessageText"] = suggestion 
        self.consoleOutput(suggestion, outputtext)
        suggestion_message = Message("suggestion", self.client.character.name, contents)
        #suggestion_message.printMessage()
        self.client.send_message(suggestion_message)

    def disproveMessage(self,disproveInput, outputtext):
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

            if (disprove_item.replace(" ","").lower() in self.client.characterInventory or disprove_item.replace(" ","").lower() in self.client.roomInventory or disprove_item.replace(" ","").lower() in self.client.weaponInventory):
                disprove_message = Message("disprove", self.client.character.name, contents)
                            #disprove_message.printMessage()
                self.client.send_message(disprove_message)
            else:
                self.consoleOutput(f"You do not have item \"{disprove_item}\" in your inventory. Please enter a different item.", outputtext)

    def accusationMessage(self, accusationInputCharacter, accusationInputRoom, accusationInputWeapon, outputtext):
            contents = {}
            accusation_suspect = accusationInputCharacter.get().title()
            contents["suspect"] = accusation_suspect

            accusation_room = accusationInputRoom.get().title()
            contents["room"] = accusation_room 

            accusation_weapon = accusationInputWeapon.get().replace(" ", "").lower()
            contents["weapon"] = accusation_weapon 

            accusation = "I accuse " + contents["suspect"] + " of committing the crime in the " + contents["room"] + " with the " + contents["weapon"]
            contents["accusationMessageText"] = accusation
            self.consoleOutput(accusation, outputtext)
            accusation_message = Message("accusation", self.client.character.name, contents)
            #accusation_message.printMessage()
            self.client.send_message(accusation_message)

    def create_widgets(self):
        # Your existing code here...
        # Replace 'self' with 'root' for widgets that should be part of the main window

        # root window (main window)
        self.master.title("Clue-Less Application")
        self.master.geometry("750x750")

        # set title
        title = Label(self, text="Clue-Less Info Board")
        title.grid(row=0, column=0, sticky='', columnspan=5)
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
        characterItems = ['Miss Scarlet','Colonel Mustard', 'Mrs. White','Mr. Green', 'Mrs. Peacock', 'Professor Plum'] 
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
        movebutton = Button(self, text="Make a Move", command= lambda: self.moveMessage(inputValMove, outputtext)).grid(column=4, row=17, columnspan=5)

        # suggesstion
        inputValSuggesstionCharacter = StringVar()
        inputValSuggesstionCharacter.set("character option")
        inputValSuggesstionWeapon = StringVar()
        inputValSuggesstionWeapon.set("weapon option")
        userInputCharacterSuggest = OptionMenu(self, inputValSuggesstionCharacter, *characterItems).grid(column=1, row=18, columnspan=1)
        UserInputSuggestWeapon = OptionMenu(self, inputValSuggesstionWeapon, *weaponItems).grid(column=2, row=18, columnspan=2)
        suggestButton = Button(self, text="Make a Suggestion", command= lambda: self.suggesstionMessage(inputValSuggesstionCharacter,inputValSuggesstionWeapon, outputtext)).grid(column=4, row=18, columnspan=5)
        
        #Disprove Set Up 
        disproveInput = StringVar()
        disproveInput.set("item to disprove")
        inventoryListNoOption = inventoryList
        inventoryListNoOption.append("can't disprove suggesstion")
        UserInputDisprove = OptionMenu(self, disproveInput, *inventoryListNoOption).grid(column=0, row=19, columnspan=5)
        disproveButton = Button(self, text="Disprove", command= lambda: self.disproveMessage(disproveInput, outputtext)).grid(column=4, row=19, columnspan=5)
        
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
        accusationButton = Button(self, text="Make Accusation", command= lambda: self.accusationMessage(accusationInputCharacter, accusationInputRoom, accusationInputWeapon, outputtext)).grid(column=4, row=20, columnspan=5)
        
        #Start thread to listen for messages from server
        data_thread = threading.Thread(target=self.checkServer, args=(self.client,outputtext,))
        data_thread.start()
 