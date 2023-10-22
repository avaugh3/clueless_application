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

if __name__ == "__main__":
    #HOST = '127.0.0.1'
    #PORT = 12345

    HOST = input("Enter Server IP Address: ")
    PORT = int(input("Enter Server Port: "))

    client = CluelessClient(HOST, PORT)
    client.connect()

    print(f"Welcome to Clue-Less!\n")
    original_character_name = input("Please enter your character name: ")
    original_character_name = original_character_name.title()

    while True:
        initial_action_message = input("Enter a message (options: move, suggestion, accusation, disprove suggestion) or quit the game (type 'exit'): ")
        
        contents = {}

        if initial_action_message == 'move':
            move_selection = input("Enter direction to move: ")
            contents["direction"] = move_selection 
            move_message = MoveMessage(original_character_name, contents)
            move_message.printMessage()
            client.send_message(move_message)

        elif initial_action_message == 'suggestion':
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

        elif initial_action_message == 'accusation':
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

        elif initial_action_message == "disprove suggestion":
            initial_action_message.replace(" ", "_").lower()

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
            
            disprove_suggestion_message = DisproveSuggestionMessage(original_character_name, contents)
            disprove_suggestion_message.printMessage()
            client.send_message(disprove_suggestion_message)

        if initial_action_message.lower() == 'exit':
            break

    client.close()