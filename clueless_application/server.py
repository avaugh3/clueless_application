import sys
import socket
import threading
import pickle
import random 
from collections import OrderedDict
from messaging.message import Message
from messaging.broadcast_message import BroadcastMessage
from messaging.specific_client_message import SpecificClientMessage
from gameAnswer import GameAnswer

class CluelessServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = OrderedDict()
        self.tempClientDict = OrderedDict()
        self.winningAnswer = GameAnswer().GenerateAnswer()
        self.charactersInventory, self.roomsInventory, self.weaponsInventory = self.winningAnswer.dealInventory()
        self.weapons = ['rope', 'leadpipe', 'knife', 'wrench', 'candlestick', 'revolver', 'dagger']
        self.rooms = ['study', 'hall', 'lounge', 'diningroom', 'kitchen', 'ballroom', 'conservatory', 'library', 'billardroom']
        self.characters = ['missscarlet', 'colonelmustard', 'missuswhite', 'mistergreen', 'missuspeacock', 'professorplum']

    def validateMove(self, client, message):
        print("Beginning Move Validation")
        direction = message.contents['direction']
        currentLocation = message.contents['currentLocation']
        newLocation = currentLocation.copy()

        if (direction == "left" or direction == "right" or direction == "up" or direction == "down"):
            if (direction == "left"):
                newLocation[1] = currentLocation[1] - 1
            elif (direction == "right"):
                newLocation[1] = currentLocation[1] + 1
            elif (direction == "up"):
                newLocation[0] = currentLocation[0] - 1
            else:
                newLocation[0] = currentLocation[0] + 1

            if (newLocation[0] < 5 and newLocation[1] < 5 and newLocation[0]>-1 and newLocation[1]>-1):
                contents = {}
                info = f"Message From Server: Move Validated, New Location is {newLocation}"
                contents["newLocation"] = newLocation
                contents["info"] = info
            
                updateMessage = Message("updateLocation", "Server", contents)
    
                self.sendMessageToSpecificClient(client, updateMessage)
                print(f"Move Validated: {message.originalCharacterName} moved from {currentLocation} to {newLocation}")
            else:
                contents = {}
                contents["info"] = f"Message From Server: Invalid move, move is out of bounds of game board!"
                updateMessage = Message("info", "Server", contents)
    
                self.sendMessageToSpecificClient(client, updateMessage)
                print(f"Invalid move, move is out of bounds of game board!")

        else:
            contents = {}
            contents["info"] = f"Message From Server: Invalid move direction \"{direction}\""
            updateMessage = Message("info", "Server", contents)
    
            self.sendMessageToSpecificClient(client, updateMessage)
            print(f"Invalid Move Direction \"{direction}\".")
     
    def validateSuggestion(self, client, message):
        print("Beginning Suggestion Validation")

        suspect = message.contents["suspect"]
        weapon = message.contents["weapon"]
        contents = {}

        if (suspect.replace(" ","").lower() not in self.characters):
            contents["info"] = f"Message From Server: Suspect \"{suspect}\" is not a valid game character"
            infoMessage = Message("info", "Server", contents)
    
            self.sendMessageToSpecificClient(client, infoMessage)
            print(f"Player {message.originalCharacterName}: Suspect \"{suspect}\" is not a valid game character")

        elif (weapon.replace(" ","").lower() not in self.weapons):
            contents["info"] = f"Message From Server: Weapon \"{weapon}\" is not a valid game weapon."
            infoMessage = Message("info", "Server", contents)
    
            self.sendMessageToSpecificClient(client, infoMessage)
            print(f"Player {message.originalCharacterName}: Weapon \"{weapon}\" is not a valid game weapon.")

        else:
            contents["info"] = f"Broadcast From Server: Player {message.originalCharacterName}: \"{message.contents['suggestionMessageText']}\""
            infoMessage = Message("info", "Server", contents)
    
            self.broadcastMessage(self.clients, infoMessage)
            print(f"Player {message.originalCharacterName}: \"{message.contents['suggestionMessageText']}\"")
       
    def validateAccusation(self, client, message):
        print("Beginning Accusation Validation")

        suspect = message.contents["suspect"]
        weapon = message.contents["weapon"]
        room = message.contents["room"]
        contents = {}

        if (suspect.replace(" ","").lower() not in self.characters):
            contents["info"] = f"Message From Server: Suspect \"{suspect}\" is not a valid game character"
            infoMessage = Message("info", "Server", contents)
    
            self.sendMessageToSpecificClient(client, infoMessage)
            print(f"Player {message.originalCharacterName}: Suspect \"{suspect}\" is not a valid game character")

        elif (weapon.replace(" ","").lower() not in self.weapons):
            contents["info"] = f"Message From Server: Weapon \"{weapon}\" is not a valid game weapon."
            infoMessage = Message("info", "Server", contents)
    
            self.sendMessageToSpecificClient(client, infoMessage)
            print(f"Player {message.originalCharacterName}: Weapon \"{weapon}\" is not a valid game weapon.")

        elif (room.replace(" ","").lower() not in self.rooms):
            contents["info"] = f"Message From Server: Room \"{room}\" is not a valid game room."
            infoMessage = Message("info", "Server", contents)
    
            self.sendMessageToSpecificClient(client, infoMessage)
            print(f"Player {message.originalCharacterName}: Room \"{room}\" is not a valid game room.")

        else:
            contents["info"] = f"Broadcast From Server: Player {message.originalCharacterName}: \"{message.contents['accusationMessageText']}\""
            infoMessage = Message("info", "Server", contents)
    
            self.broadcastMessage(self.clients, infoMessage)
            print(f"Player {message.originalCharacterName}: \"{message.contents['accusationMessageText']}\"")
            
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

    def startGame(self):
        print("Deal inventory to joined clients.")
        
        contents = {}
        
        contents["weapon"] = "dagger"
            
        updateMessage = Message("addWeapon", "Server", contents)

        random.shuffle(self.weapons)
        random.shuffle(self.rooms)
        random.shuffle(self.characters)

        for client, item in zip(self.clients.keys(), self.weapons):
            contents["weapon"] = item
            updateMessage = Message("addWeapon", "Server", contents)

            self.sendMessageToSpecificClient(client, updateMessage)
        

        print("Output game board.")

        print("Send move notifcation to first player.")

    """
    Switch-Case to Trigger Methods Based on Message Contents
    """
    def processMessage(self, message, client):
        loaded_msg = pickle.loads(message)
        print(f"Processing Message from Client {self.clients[client]}: {'type:', loaded_msg.type, 'originalCharacterName:', loaded_msg.originalCharacterName, 'contents:', loaded_msg.contents}")

        if loaded_msg.type == 'move':
            self.validateMove(client, loaded_msg)

        elif loaded_msg.type == 'suggestion':
            self.validateSuggestion(client, loaded_msg)

        elif loaded_msg.type == 'accusation':
            self.validateAccusation(client, loaded_msg)

        elif loaded_msg.type == 'disprove':
            self.validateDisprove(client, loaded_msg)
        else:
            print(f"Processing Failed: Unknown Message Type \"{loaded_msg.type}\"")

    def sendMessageToSpecificClient(self, client, message):
        pickled_msg = pickle.dumps(message)
        
        client.send(pickled_msg)

    """
    Sends message to all Clients 
    """
    def broadcastMessage(self, clients, message):
        pickled_msg = pickle.dumps(message)
        
        for client in clients.keys():
            client.send(pickled_msg)

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
        
    
    """
    When Client Sends Message, New Thread is Opened to Process the Message
    """
    def handle_client(self, client):
        self.startGame()
        while True:
            try:
                #contents = {}
                data = client.recv(2048)
                if not data:
                    break

                self.processMessage(data, client)
    
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