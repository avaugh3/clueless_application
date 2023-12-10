import sys
import socket
import threading
import pickle
import random 
import time
from collections import OrderedDict
from messaging.message import Message
#from messaging.broadcast_message import BroadcastMessage
#from messaging.specific_client_message import SpecificClientMessage
from gameAnswer import GameAnswer
import itertools

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
        self.playersReady = 0
        self.currentSuggestion = ["dagger", "study", "rope"]

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

                contents["info"] = f"Move Validated: {message.originalCharacterName} moved from {currentLocation} to {newLocation}"
                broadcastMessage = Message("info", "Server", contents)

                self.broadcastMessage(self.clients, broadcastMessage)
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
            self.currentSuggestion = []
            self.currentSuggestion.append(suspect.replace(" ","").lower())
            self.currentSuggestion.append(weapon.replace(" ","").lower())

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
            if (suspect.replace(" ","").lower() == self.winningAnswer.character.replace(" ","").lower() and 
                weapon.replace(" ","").lower() == self.winningAnswer.weapon.replace(" ","").lower() and 
                room.replace(" ","").lower() == self.winningAnswer.room.replace(" ","").lower()):
                
                contents["info"] = f"Broadcast From Server: Accusation was correct! \n Player {message.originalCharacterName}: \"{message.contents['accusationMessageText']}\" \n Player {message.originalCharacterName} wins! \n Thanks for playing!"
                infoMessage = Message("info", "Server", contents)
    
                self.broadcastMessage(self.clients, infoMessage)    
                print(f"Accusation was correct! \n Player {message.originalCharacterName}: \"{message.contents['accusationMessageText']}\" \n Player {message.originalCharacterName} wins! \n Thanks for playing!")
            
                self.endGame()

            else:
                contents["info"] = f"Broadcast From Server: Accusation Incorrect. \n Player {message.originalCharacterName}: \"{message.contents['accusationMessageText']}\" \n Player {message.originalCharacterName} is disqualified from game."
                infoMessage = Message("info", "Server", contents)
    
                self.broadcastMessage(self.clients, infoMessage)    
                print(f"Accusation Incorrect. \n Player {message.originalCharacterName}: \"{message.contents['accusationMessageText']}\" \n Player {message.originalCharacterName} is disqualified from game.")
                     
    def validateDisprove(self, client, message):
        print("Trigger Validating Disprove")

        item = message.contents['item']

        if (item.replace(" ","").lower() in self.currentSuggestion):
            print(f"Player {message.originalCharacterName} disproved item \"{item}\". {item} is not in winning answer.")

            contents = {}
            contents['info'] = f"Player {message.originalCharacterName} disproved item \"{item}\". {item} is not in winning answer."

            infoMessage = Message("info", "Server", contents)

            self.broadcastMessage(self.clients,infoMessage)
        else:
            print(f"Item \"{item}\" is not in the current suggestion. Cannot disprove suggestion. Please try again.")

            contents = {}
            contents['info'] = f"Item \"{item}\" is not in the current suggestion. Cannot disprove suggestion. Please try again."

            infoMessage = Message("info", "Server", contents)

            self.sendMessageToSpecificClient(client,infoMessage)

    def determineGameWinner(self):
        print("Determining if There is a Game Winner")
    
    def endGame(self):
        print("Shutting down Clue-Less Server...")
        for client in self.clients.keys():
            client.close()
        sys.exit(0)

    def startGame(self):
        print("Dealing Rooms, Weapons, and Characters to all Joined Players")
        num_clients = len(self.clients)

        rooms_per_client = len(self.roomsInventory) // num_clients
        rooms_remainder = len(self.roomsInventory) % num_clients
        rooms_start_index = 0

        weapons_per_client = len(self.weaponsInventory) // num_clients
        weapons_remainder = len(self.weaponsInventory) % num_clients
        weapons_start_index = 0

        characters_per_client = len(self.charactersInventory) // num_clients
        characters_remainder = len(self.charactersInventory) % num_clients
        characters_start_index = 0

        # Iterate through the clients and distribute the rooms
        for client in self.clients.keys():
            contents = {}
            # Calculate the end index for slicing
            rooms_end_index = rooms_start_index + rooms_per_client + (1 if rooms_remainder > 0 else 0)
            weapons_end_index = weapons_start_index + weapons_per_client + (1 if weapons_remainder > 0 else 0)
            characters_end_index = characters_start_index + characters_per_client + (1 if characters_remainder > 0 else 0)
            
            # Get the portion of weapons for the current client
            rooms_portion = self.roomsInventory[rooms_start_index:rooms_end_index]
            weapons_portion = self.weaponsInventory[weapons_start_index:weapons_end_index]
            characters_portion = self.charactersInventory[characters_start_index:characters_end_index]
            
            # Update the contents dictionary for the current client
            contents['rooms'] = rooms_portion
            contents['weapons'] = weapons_portion
            contents['characters'] = characters_portion

            # Create and send the message to the current client
            updateMessage = Message("loadInventory", "Server", contents)
            self.sendMessageToSpecificClient(client, updateMessage)
            self.broadcastMessage(self.clients, "ALL Inventories should be sent out")
            # Update the start index for the next iteration
            rooms_start_index = rooms_end_index
            rooms_remainder -= 1

            weapons_start_index = weapons_end_index
            weapons_remainder -= 1

            characters_start_index = characters_end_index
            characters_remainder -= 1
        
            
    """
    Switch-Case to Trigger Methods Based on Message Contents
    """
    def processMessage(self, message, client):
        loaded_msg = pickle.loads(message)
        print(f"Processing Message from Client {self.clients[client]}: {'type:', loaded_msg.type, 'originalCharacterName:', loaded_msg.originalCharacterName, 'contents:', loaded_msg.contents}")

        if loaded_msg.type == 'ready':
            self.playersReady += 1
            print(f"Player {loaded_msg.originalCharacterName} is Ready to Begin")

            if (self.playersReady == len(self.clients)):
                print("Clue-Less Game is Starting!")
                print(f"\nWinning Answer Generated: \n- Room: {self.winningAnswer.room}\n- Character: {self.winningAnswer.character}\n- Weapon: {self.winningAnswer.weapon}\n")
                
                self.startGame()

        elif loaded_msg.type == 'move':
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