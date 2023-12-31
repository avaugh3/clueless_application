import sys
import socket
import threading
import pickle
import random 
from collections import OrderedDict
from messaging.message import Message
from messaging.move_message import MoveMessage 
from messaging.suggestion_message import SuggestionMessage
from messaging.accusation_message import AccusationMessage
from messaging.disprove_suggestion_message import DisproveSuggestionMessage
from messaging.broadcast_message import BroadcastMessage
from messaging.specific_client_message import SpecificClientMessage

class CluelessServer:
    
    weapons = ['rope', 'lead pipe', 'knife', 'wrench', 'candlestick', 'revolver']
    rooms = ['study', 'hall', 'lounge', 'dining room', 'kitchen', 'ballroom', 'conservatory', 'library', 'billard room']
    characters = ['miss scarlet', 'colonel mustard', 'mrs. white', 'mr. green', 'mrs. peacock', 'professor plum']
    answerArray = []

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.clients = []
        self.clients = OrderedDict()
        self.tempClientDict = OrderedDict()

    # Function to create the random answer of items. This will be triggered when the user presses the begin game function
    # TODO: Possibly add the division of items out into this function. 
    def createAnswer(self):
        weaponChoice = random.randint(0,5)
        roomChoice = random.randint(0, 8)
        characterChoice = random.randint(0, 5)
        answerArray = [self.weapons[weaponChoice], self.rooms[roomChoice], self.characters[characterChoice]]
        print("A new random answer has been created. The game can now begin")

    # Takes in character trying to move, where they are trying to move to, is it a hallway or room?
    # Character: person making the move
    # location: where they are moving to will either be a Hall object or Room Object
    # isHallway: boolean if this is hallway or not so that can check if is occupied
    def validateMove(self, direction):
        print("Trigger Validating Move")
        
        """
        if location.isHallway:
            if location.isOccupied:
                # sent to single player
                print("Sorry that hallway is occupied already. Please try again.")
            else:
                # sent to everybody
                print(f"Character {character.name} move is successful to {location.name}")
                character.location = location
                #TODO: Update UI
        else:
            # send to everybody
            print(f"Character {character.name} move is successful to {location.name}")
            character.location = location
            #TODO: Update UI
        """
    

        """
         Server will need to get the room the Character is making the Suggestion in 
         to then insert this into the client's suggestion from their message's 
         content['suggestion'] entry. 
        
         The server can now begin the validation because the server has the full Suggestion 
         with Character (suspect), Room, and Weapon.
        """
    # Takes in the character making suggesstion, where they currently are located, Weapon and character making a suggesstion.
    # Character: Person making the move
    # location: where the character is located to make suggesstion
    # weaponItem: the weapon they are suggessting 
    # suggesstedCharacter: the character they are suggessting
    def validateSuggestion(self, weaponItem, suggestedCharacter):
        print("Trigger Validating Suggestion")
        """

        Server will need to check that the client has their one Accusation left. 
        If not, the client cannot make another Accusation  

        if character.madeAccusation != True:
            if character.location.isRoom:
                if weaponItem.name not in self.weapons: 
                    print('That is not a valid weapon item.')
                    return
                if suggesstedCharacter.name not in self.characters:
                    print('That is not a valid character.') 
                    return
                # send to everybody
                print(f'Player {character.name} has made a valid suggesstion with {suggesstedCharacter.name} in the {location.name} with the {weaponItem.name} ')
                #TODO: Call the disprove for other players to disprove
            else:
                # send to individual
                print("You are not in a room and therefore cannot make a suggestion.")
        else:
            # send to individual
            print("You have made an incorrect accusation before. You cannot make a suggestion")
        """
            
    """
    Server will need to check that the client has their one Accusation left. 
    If not, the client cannot make another Accusation  
    """
    def validateAccusation(self, room, weapon, suggestedCharacter):
        print("Trigger Validating Accusation")
        """
        if character.madeAccusation != True:
            if weapon.name not in self.weapons: 
                print('That is not a valid weapon item.') 
                return
            if suggestedCharacter.name not in self.characters:
                print('That is not a valid character.') 
                return
            if room.name not in self.rooms: 
                print('That is not a valid room item.') 
                return
            # send to everybody
            print(f'Player {character.name} has made an accusation with {suggestedCharacter.name} in the {room.name} with the {weapon.name} ')
            # check answer
            if weapon.name == self.answerArray[0] & room.name == self.answerArray[1] & suggestedCharacter.name == self.answerArray[2]:
                # send to everybody
                print(f'Congrats! Player {character.name} has correctly made an Accusation and won the game!')
                self.endGame()
            else:
                # send to individual player
                print('Sorry! That is incorrect. Your game is over and you cannot make any more suggesstions/accusations but you can aid your fellow players to disprove suggestions.')
                character.madeAccusation = True
        else:
            # send to individual
            print("You have made an incorrect accusation before. You cannot make another one.")
        """
            
    # This gets called after someone makes a suggestion and prompts the other players to disprove it. 
    # takes in boolean if can or not disprove, and item
    def validateDisprove(self, canDisprove, itemType, item):
        print("Trigger Validating Disprove")
        if canDisprove:
            # send this to client who made the suggestion 
            print(f'Hey player! Someone has been able to disprove your suggestion with this item: {itemType} - {item}')
        else:
            print("This player cant disprove it. On to the next one")
            #TODO: Send message to next player in list to disprove

    def determineGameWinner(self):
        print("Determining if There is a Game Winner")
    
    def endGame(self):
        print("Winner Determined, Exiting Game")

    """
    Switch-Case to Trigger Methods Based on Message Contents
    """
    def processMessage(self, message, client):
        loaded_msg = pickle.loads(message)
        print(f"Processing Message from Client {self.clients[client]}: {'type:', loaded_msg.type, 'originalCharacterName:', loaded_msg.original_character_name, 'contents:', loaded_msg.contents}")

        if loaded_msg.type == 'move':
            self.validateMove(loaded_msg.contents['direction'])
            self.broadcastMessage(self.clients, f"Player {loaded_msg.original_character_name} made move {loaded_msg.contents['direction']}")
            
        elif loaded_msg.type == 'suggestion':
            """
            Method or logic needed to get the client's current room 
            since their suggestion will not include the room 
            because it is implied which room is in the suggestion 
            since a Suggestion can only be made including the room 
            the Suggestion was made in.
            """ 
            self.validateSuggestion(loaded_msg.contents['weapon'], loaded_msg.contents['suspect'])
            self.broadcastMessage(self.clients, f"Player {loaded_msg.original_character_name}: {loaded_msg.contents['suggestionMessageText']}")
        elif loaded_msg.type == 'accusation':
            self.validateAccusation(loaded_msg.contents['room'], loaded_msg.contents['weapon'],loaded_msg.contents['suspect'])
            self.broadcastMessage(self.clients, f"Player {loaded_msg.original_character_name}: {loaded_msg.contents['accusationMessageText']}")
        elif loaded_msg.type == 'disprove':
            self.validateDisprove(loaded_msg.contents['canDisproveSuggestion'], loaded_msg.contents['itemType'], loaded_msg.contents['item'])
        else:
            print(f"Processing Failed: Unknown Message Type \"{loaded_msg.type}\"")

    """
    Sends message to all Clients 
    """
    def broadcastMessage(self, clients, message):
        try:
            contents = {}
            contents["broadcastMessageText"] = f"\nBroadcast from Server: [{message}]\n"
            broadcast_message_instance = BroadcastMessage(contents)

            for client in clients.keys():
                client.send(broadcast_message_instance.contents["broadcastMessageText"].encode('utf-8'))

        except Exception as e:
            print(f"Error: {e}")  

    def playerTurnNotification(self, client):
        message = "It's your turn to make an action!"
        client.send(message.encode('utf-8'))

    """
    Starts Server Listening for Client Connections
    """
    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(6)
        print(f"Server is listening on {self.host}:{self.port}")

        while True:
            client, addr = self.socket.accept()
            print(f"Accepted connection from {addr}")

            self.clients[client] = addr

            self.broadcastMessage(self.clients, f"New client added to the Clue-Less game {addr}")

            if (len(self.clients) == 1):
                self.playerTurnNotification(client)
            
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

    def sendMessageToSpecificClient(self, data, client, message):
        try:
            contents = {}
            loaded_msg = pickle.loads(data)

            contents["specificClientMessageText"] = message 
            specific_client_message_instance = SpecificClientMessage(loaded_msg.original_character_name, contents)

            client.send(specific_client_message_instance.contents["specificClientMessageText"].encode('utf-8'))
            print(f"Sent response to specific client with Player Name: {loaded_msg.original_character_name}")
        except Exception as e:
            print(f"Error: {e}")        
    
    """
    When Client Sends Message, New Thread is Opened to Process the Message
    """
    def handle_client(self, client):
        while True:
            try:
                contents = {}
                data = client.recv(2048)
                if not data:
                    break

                self.processMessage(data, client)

                response = f"Message Received by Server {self.host}:{self.port}"
                  
                self.sendMessageToSpecificClient(data, client, response)
    
            except Exception as e:
                print(f"Error: {e}")
                break
        
        print(f"Lost Connection to Client {self.clients[client]}")
        client.close()
        del self.clients[client]

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 12345

    server = CluelessServer(HOST, PORT)
    server.start()