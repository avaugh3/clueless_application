import socket
import pickle
from messaging.message import Message
from messaging.move_message import MoveMessage 
from messaging.suggestion_message import SuggestionMessage
from messaging.accusation_message import AccusationMessage
from messaging.disprove_suggestion_message import DisproveSuggestionMessage

class CluelessClient:
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
        send_message(self, 'move')


    def makeSuggesstion(self):
        print(f"Player {self.host} decided to make a sugesstion")
        weapon = input('Please enter the weapon you think was used: ')
        suggesstedCharacter = input('Please enter who you think committed the crime: ')
        #TODO figure out character and location
        #validateSuggestion(self, character, character.location, weapon, suggesstedCharacter)
        send_message(self, 'suggestion')

    def makeAccusation(self):
        print(f"Player {self.host} decided to make an accusation.")
        room = input('Please enter the room you think the crime occured: ')
        weapon = input('Please enter the weapon you think was used: ')
        suggesstedCharacter = input('Please enter who you think committed the crime: ')
        # validateAccusation(self, self.host, room, weapon, suggesstedCharacter)
        send_message(self, 'accusation')

    def disproveSuggestion(self):
        item = input(f"Player {self.host} please enter the item to disprove the other player. If you can not disprove enter no")
        if item == 'no':
           # validateDisprove(self, false, item)
           send_message(self, 'disprove')
        else:
           # validateDisprove(self, true, item)
           send_message(self, 'disprove')
    

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
            print("Processing Failed: Unknown Message");

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 12345

    client = CluelessClient(HOST, PORT)
    client.connect()

    while True:
        initial_message = input("Enter a message (options: move, suggestion, accusation, disprove suggestion) or quit the game (type 'exit'): ")
        
        contents = {}

        if initial_message == 'move':
            move_selection = input("Enter direction to move: ")
            contents["direction"] = move_selection 
            move_message = MoveMessage(contents)
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

            suggestion_message = SuggestionMessage(contents)
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

            accusation_message = AccusationMessage(contents)
            accusation_message.printMessage()
            client.send_message(accusation_message)

        elif initial_message == "disprove suggestion":
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
            
            disprove_suggestion_message = DisproveSuggestionMessage(contents)
            disprove_suggestion_message.printMessage()
            client.send_message(disprove_suggestion_message)

        if initial_message.lower() == 'exit':
            break

    client.close()