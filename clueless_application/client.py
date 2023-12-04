import socket
import pickle
import sys
import platform
import time
import random
from messaging.message import Message
from Inventory.character import Character
from Inventory.inventory import Inventory


class CluelessClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.character = Character()
        self.inventory = Inventory()
        self.playerName = None
        self.boardLocation = [random.randint(0, 4), random.randint(0, 4)]
        self.characterInventory = []
        self.roomInventory = []
        self.weaponInventory = []
        self.ready = False
        self.gameStarted = False
        

    def setBoardLocation(self,location):
        self.boardLocation = location

    def connect(self):
        self.socket.connect((self.host, self.port))
        print(f"Connected to {self.host}:{self.port}")

    def send_message(self, message):
        pickled_msg = pickle.dumps(message)
        
        self.socket.send(pickled_msg)
        #response = self.socket.recv(1024).decode('utf-8')
        
        #Server Response
        #print(response)

    def processMessage(self, message):
        loaded_msg = pickle.loads(message)

        if (loaded_msg.type == "updateLocation"):
            print(loaded_msg.contents["info"])
            self.setBoardLocation(loaded_msg.contents['newLocation'])

        elif (loaded_msg.type == "info"):
            print(loaded_msg.contents["info"])

        elif (loaded_msg.type == "loadInventory"):
            print("Loading Client Inventory")
            self.roomInventory = loaded_msg.contents['rooms']
            self.weaponInventory = loaded_msg.contents['weapons']
            self.characterInventory = loaded_msg.contents['characters']
            self.gameStarted = True

    def handle_read(self):
        message = self.recv(1024)
        self.log.info('Received message: %s', )

    def close(self):
        self.socket.close()

    def inputWithTimeout(self, prompt, timeout, print_prompt=True):
        if print_prompt:
            print()
            if (self.ready and self.gameStarted):
                print(f"Player Name: {self.playerName}")
                print(f"- Board Location: {self.boardLocation}")
                print(f"- Room Inventory: {self.roomInventory}")
                print(f"- CharacterInventory: {self.characterInventory}")
                print(f"- Weapon Inventory: {self.weaponInventory}\n")
            print(prompt)

        start_time = time.time()
        input_data = None

        while True:
            if platform.system() == 'Windows':
                import msvcrt
                if msvcrt.kbhit():
                    input_data = msvcrt.getche().decode()
                    break
            else:
                import select
                rlist, _, _ = select.select([sys.stdin], [], [], 0)
                if rlist:
                    input_data = sys.stdin.readline().rstrip('\n')
                    break

            if time.time() - start_time > timeout:
                break

        return input_data

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 12345

    HOST = input("Enter IP Address of ClueLess Server: ")
    PORT = int(input("Enter Port Number of Clueless Server: "))

    INPUT_TIMEOUT = 1 #seconds
    print_prompt = True

    client = CluelessClient(HOST, PORT)
    client.connect()
    client.socket.settimeout(0.1)

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

    while True:
        #Check for server message each loop iteration
        try:
            data = client.socket.recv(2048) #recv(1024).decode('utf-8')
            if data:
                client.processMessage(data)

                print_prompt = True
        except:
            pass
        
        if (client.ready and client.gameStarted):
            initial_message = client.inputWithTimeout("Enter a message (options: move, suggestion, accusation, disprove) or quit the game (type 'exit'): ", INPUT_TIMEOUT, print_prompt)
            print_prompt = False
        elif (not client.ready):
            initial_message = client.inputWithTimeout("Type 'Ready' to Notify Server You are Ready to Begin: ", INPUT_TIMEOUT, print_prompt)
            print_prompt = False
        else:
            initial_message = client.inputWithTimeout("Waiting for Server to start game...", INPUT_TIMEOUT, print_prompt)
            print_prompt = False
    
        if (initial_message != None):
            print_prompt = True
            contents = {}
            
            if initial_message == 'ready':
                ready_message = Message("ready", original_character_name, None)
                client.send_message(ready_message)
                client.ready = True
                

            elif initial_message == 'move':
                move_selection = input("Enter direction to move: ")
                contents["direction"] = move_selection 
                contents["currentLocation"] = client.boardLocation
        
                move_message = Message("move", original_character_name, contents)
                #move_message.printMessage()
                client.send_message(move_message)

            elif initial_message == 'suggestion':
                suggestion_suspect = input("Choose a Suspect: (options: Miss Scarlet, Colonel Mustard, Missus White, Mister Green, Missus Peacock, Professor Plum): ")
                suggestion_suspect = suggestion_suspect.title()
                contents["suspect"] = suggestion_suspect

                suggestion_weapon = input("Choose a Weapon: (options: Candlestick, Dagger, Revolver, Lead Pipe, Wrench, Rope): ")
                suggestion_weapon.replace(" ", "").lower()
                contents["weapon"] = suggestion_weapon 

                suggestion = f"I suggest the crime was committed in {client.boardLocation} by " + contents["suspect"] + " with the " + contents["weapon"]
                contents["suggestionMessageText"] = suggestion 

                suggestion_message = Message("suggestion", original_character_name, contents)
                #suggestion_message.printMessage()
                client.send_message(suggestion_message)

            elif initial_message == 'accusation':
                accusation_suspect = input("Choose a Suspect: (options: Miss Scarlet, Colonel Mustard, Missus White, Mister Green, Missus Peacock, Professor Plum): ")
                accusation_suspect = accusation_suspect.title()
                contents["suspect"] = accusation_suspect

                accusation_room = input("Choose a Room: (options: Hall, Lounge, Dining Room, Study, Kitchen, Ballroom, Conservatory, Billard Room, Library): ")
                accusation_room = accusation_room.title()
                contents["room"] = accusation_room 

                accusation_weapon = input("Choose a Weapon: (options: Candlestick, Dagger, Revolver, Lead Pipe, Wrench, Rope): ")
                accusation_weapon.replace(" ", "").lower()
                contents["weapon"] = accusation_weapon 

                accusation = "I accuse " + contents["suspect"] + " of committing the crime in the " + contents["room"] + " with the " + contents["weapon"]
                contents["accusationMessageText"] = accusation

                accusation_message = Message("accusation", original_character_name, contents)
                #accusation_message.printMessage()
                client.send_message(accusation_message)

            elif initial_message == 'disprove':
                initial_message.replace(" ", "_").lower()

                is_disprove_suggestion_possible = input("Can you disprove the Suggestion? (true/false): ")
                is_disprove_suggestion_possible = is_disprove_suggestion_possible.capitalize()
                contents["canDisproveSuggestion"] = is_disprove_suggestion_possible 

                print(is_disprove_suggestion_possible)

                if is_disprove_suggestion_possible:
 
                    #item_type = input("Which inventory item type do you have? (options: Suspect, Room, Weapon): ")
                    #inventory_type_to_disprove_suggestion = inventory_type_to_disprove_suggestion.capitalize()

                    disprove_item = input("What is the specific value of the inventory item? (e.g., Dagger, Colonel Mustard, Lounge): ")

                    #Just add itemType and item to message contents --------------
                    #contents['itemType'] = inventory_type_to_disprove_suggestion
                    contents['item'] = disprove_item
                    #-------------------------------------------------------------

                if (disprove_item.replace(" ","").lower() in client.characterInventory or disprove_item.replace(" ","").lower() in client.roomInventory or disprove_item.replace(" ","").lower() in client.weaponInventory):
                    disprove_message = Message("disprove", original_character_name, contents)
                    #disprove_message.printMessage()
                    client.send_message(disprove_message)
                else:
                    print(f"You do not have item \"{disprove_item}\" in your inventory. Please enter a different item.")

            elif (initial_message != 'exit'):
                print(f"Invalid Message Type: {initial_message}")

            if initial_message.lower() == 'exit':
                break

    client.close()
