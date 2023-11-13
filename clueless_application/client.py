import socket
import pickle
import sys
import select
import time
import platform 
from messaging.message import Message
from messaging.move_message import MoveMessage 
from messaging.suggestion_message import SuggestionMessage
from messaging.accusation_message import AccusationMessage
from messaging.disprove_suggestion_message import DisproveSuggestionMessage

class CluelessClient:

    rooms = ['study', 'hall', 'lounge', 'dining room', 'kitchen', 'ballroom', 'conservatory', 'library', 'billard room']

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.host, self.port))
        print(f"Connected to {self.host}:{self.port}")

    def send_message(self, message):
        pickled_msg = pickle.dumps(message)
        
        self.socket.send(pickled_msg)
        response = self.socket.recv(1024).decode('utf-8')
        
        #Server Response
        print(response)

    def handle_read(self):
        message = self.recv(1024)
        self.log.info('Received message: %s', )

    def close(self):
        self.socket.close()

    def makeMove(self):
        print(f"Player {self.host} decided to make a move")
        #TODO Figure out how we get move value
        # TODO figure out how to get character value
        # validateMove(self, self.character, move))
        self.send_message('move')


    def makeSuggesstion(self):
        print(f"Player {self.host} decided to make a sugesstion")
        weapon = input('Please enter the weapon you think was used: ')
        suggesstedCharacter = input('Please enter who you think committed the crime: ')
        #TODO figure out character and location
        #validateSuggestion(self, character, character.location, weapon, suggesstedCharacter)
        self.send_message('suggestion')

    def makeAccusation(self):
        print(f"Player {self.host} decided to make an accusation.")
        room = input('Please enter the room you think the crime occured: ')
        weapon = input('Please enter the weapon you think was used: ')
        suggesstedCharacter = input('Please enter who you think committed the crime: ')
        # validateAccusation(self, self.host, room, weapon, suggesstedCharacter)
        self.send_message('accusation')

    def disproveSuggestion(self):
        item = input(f"Player {self.host} please enter the item to disprove the other player. If you can not disprove enter no")
        if item == 'no':
           # validateDisprove(self, false, item)
           self.send_message('disprove')
        else:
           # validateDisprove(self, true, item)
           self.send_message('disprove')
    

    def processMessage(self, message):
        print(f"Processing Message: {message}")

        if message == 'move':
            self.validateMove()
        elif message == 'suggestion':
            self.validateSuggestion()
        elif message == 'accusation':
            self.validateAccusation()
        elif message == 'disprove':
            self.validateDisprove()
        else:
            print("Processing Failed: Unknown Message")
    
    """
    #This doesn't work on Windows for some reason
    def inputWithTimeout(self, prompt, timeout, print_prompt):
        if print_prompt:
            print(prompt)
        rlist, _, _ = select.select([sys.stdin], [], [], timeout)
        if rlist:
            return sys.stdin.readline().strip()
        else:
            return None
    """
    def inputWithTimeout(self, prompt, timeout, print_prompt=True):
        if print_prompt:
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
    original_character_name = input("Please enter your character name | miss scarlet (!), colonel mustard ($), missus white (*), mister green (^), missus peacock (@), professor plum (&): ")
    original_character_name = original_character_name.title()

    while True:
        #Check for server message each loop iteration
        try:
            data = client.socket.recv(1024).decode('utf-8')
            if data:
                print(data+'\n')
                print_prompt = True
        except:
            pass

        initial_message = client.inputWithTimeout("Enter a message (options: move, suggestion, accusation, disprove) or quit the game (type 'exit'): ", INPUT_TIMEOUT, print_prompt)
        print_prompt = False

        if (initial_message != None):
            print_prompt = True
            contents = {}
            if initial_message == 'move':
                move_selection = input("Enter direction to move: ")
                contents["direction"] = move_selection 
                move_message = MoveMessage(original_character_name, contents)
                move_message.printMessage()
                client.send_message(move_message)

            elif initial_message == 'suggestion':
                # Room is not included in the Suggestion because 
                # the server will know, based on the client which Room their 
                # character is in 
                suggestion_suspect = input("Choose a Suspect: (options: Miss Scarlet, Colonel Mustard, Missus White, Mister Green, Missus Peacock, Professor Plum): ")
                suggestion_suspect = suggestion_suspect.title()
                contents["suspect"] = suggestion_suspect

                suggestion_weapon = input("Choose a Weapon: (options: Candlestick, Dagger, Revolver, Lead Pipe, Wrench, Rope): ")
                suggestion_weapon.replace(" ", "").lower()
                contents["weapon"] = suggestion_weapon 

                suggestion = "I suggest the crime was committed in [room_name_server_to_determine] by " + contents["suspect"] + " with the " + contents["weapon"]
                contents["suggestionMessageText"] = suggestion 

                suggestion_message = SuggestionMessage(original_character_name, contents)
                suggestion_message.printMessage()
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

                accusation_message = AccusationMessage(original_character_name, contents)
                accusation_message.printMessage()
                client.send_message(accusation_message)

            elif initial_message == 'disprove':
                initial_message.replace(" ", "_").lower()

                is_disprove_suggestion_possible = input("Can you disprove the Suggestion? (true/false): ")
                is_disprove_suggestion_possible = is_disprove_suggestion_possible.capitalize()
                contents["canDisproveSuggestion"] = is_disprove_suggestion_possible 

                print(is_disprove_suggestion_possible)

                if is_disprove_suggestion_possible:

                    # In the future, can check if player has more than one of the items from the Suggestion
                    # Here, only considering one case, which is at minimum, the the player has at least 
                    # one card in their inventory that is within the Suggestion (and does not have any other 
                    # cards from the Suggestion)
                    # In the future, we'll also want to provide input validation 
                    inventory_type_to_disprove_suggestion = input("Which inventory item type do you have? (options: Suspect, Room, Weapon): ")
                    inventory_type_to_disprove_suggestion = inventory_type_to_disprove_suggestion.capitalize()

                    inventory_value_to_disprove_suggestion = input("What is the specific value of the inventory item? (e.g., if a Suspect, Colonel Mustard): ")

                    #Just add itemType and item to message contents --------------
                    contents['itemType'] = inventory_type_to_disprove_suggestion
                    contents['item'] = inventory_value_to_disprove_suggestion
                    #-------------------------------------------------------------

                    """
                    if inventory_type_to_disprove_suggestion == 'Suspect' or inventory_type_to_disprove_suggestion == 'Room':
                        inventory_value_to_disprove_suggestion = inventory_value_to_disprove_suggestion.title()
                    else:
                        inventory_value_to_disprove_suggestion = inventory_value_to_disprove_suggestion.lower()
                        
                    if inventory_type_to_disprove_suggestion == 'Suspect':
                        contents["hasSuspectInSuggestion"] = True 
                        contents["showSuspectToPlayerWithSuggestion"] = inventory_value_to_disprove_suggestion
                        contents["hasRoomInSuggestion"] = False 
                        contents["showRoomToPlayerWithSuggestion"] = "non-applicable"
                        contents["hasWeaponInSuggestion"] = False 
                        contents["showWeaponToPlayerWithSuggestion"] = "non-applicable"    

                    elif inventory_type_to_disprove_suggestion == 'Room':
                        contents["hasSuspectInSuggestion"] = False
                        contents["showSuspectToPlayerWithSuggestion"] = "non-applicable"
                        contents["hasRoomInSuggestion"] = True
                        contents["showRoomToPlayerWithSuggestion"] = inventory_value_to_disprove_suggestion
                        contents["hasWeaponInSuggestion"] = False 
                        contents["showWeaponToPlayerWithSuggestion"] = "non-applicable" 

                    elif inventory_type_to_disprove_suggestion == 'Weapon':
                        contents["hasSuspectInSuggestion"] = False
                        contents["showSuspectToPlayerWithSuggestion"] = "non-applicable"
                        contents["hasRoomInSuggestion"] = False 
                        contents["showRoomToPlayerWithSuggestion"] = "non-applicable"
                        contents["hasWeaponInSuggestion"] = True
                        contents["showWeaponToPlayerWithSuggestion"] = inventory_value_to_disprove_suggestion
                
                else:
                    contents["hasSuspectInSuggestion"] = False
                    contents["showSuspectToPlayerWithSuggestion"] = "non-applicable"
                    contents["hasRoomInSuggestion"] = False 
                    contents["showRoomToPlayerWithSuggestion"] = "non-applicable"
                    contents["hasWeaponInSuggestion"] = False 
                    contents["showWeaponToPlayerWithSuggestion"] = "non-applicable"  
                """
                
                disprove_suggestion_message = DisproveSuggestionMessage(original_character_name, contents)
                disprove_suggestion_message.printMessage()
                client.send_message(disprove_suggestion_message)

            #elif (initial_message != 'exit'):
            #    print(f"Invalid Message Type: {initial_message}")
            
            if initial_message.lower() == 'exit':
                break

    client.close()
