import socket
import threading
import pickle
from collections import OrderedDict
from messaging.message import Message
from messaging.move_message import MoveMessage 
from messaging.suggestion_message import SuggestionMessage
from messaging.accusation_message import AccusationMessage
from messaging.disprove_suggestion_message import DisproveSuggestionMessage
from messaging.broadcast_message import BroadcastMessage
from messaging.specific_client_message import SpecificClientMessage

class CluelessServer():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = OrderedDict()
        self.tempClientDict = OrderedDict()

    def validateMove(self):
        print("Validating Move")
    
    def validateSuggestion(self):
        """
         Server will need to get the room the Character is making the Suggestion in 
         to then insert this into the client's suggestion from their message's 
         content['suggestion'] entry. 
        
         The server can now begin the validation because the server has the full Suggestion 
         with Character (suspect), Room, and Weapon.
        """
        print("Validating Suggestion")
    
    def validateAccusation(self):
        """
        Server will need to check that the client has their one Accusation left. 
        If not, the client cannot make another Accusation  
        """
        print("Validating Accusation")

    def validateDisprove(self):
        print("Validating Disprove")

    def updateGameBoard(self):
        print("Update Game Board")

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
            self.validateMove()
        elif loaded_msg.type == 'suggestion':
            """
            Method or logic needed to get the client's current room 
            since their suggestion will not include the room 
            because it is implied which room is in the suggestion 
            since a Suggestion can only be made including the room 
            the Suggestion was made in.
            """ 
            self.validateSuggestion()
        elif loaded_msg.type == 'accusation':
            self.validateAccusation()
        elif loaded_msg.type == 'disprove':
            self.validateDisprove()
        else:
            print(f"Processing Failed: Unknown Message Type \"{loaded_msg.type}\"")

    """
    Sends message to all Clients 
    """
    def broadcastMessage(self, clients, message):
        try:
            contents = {}
            contents["broadcastMessageText"] = message
            broadcast_message_instance = BroadcastMessage(contents)

            for c in clients:
                c.send(broadcast_message_instance.contents["broadcastMessageText"].encode('utf-8'))

        except Exception as e:
            print(f"Error: {e}")  

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

            self.broadcastMessage(self.clients, "New client added to the Clue-Less game")
            
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

    def sendMessageToSpecificClient(self, data, client, message):
        try:
            contents = {}
            loaded_msg = pickle.loads(data)

            contents["specificClientMessageText"] = message 
            specific_client_message_instance = SpecificClientMessage(loaded_msg.original_character_name, contents)

            client.send(specific_client_message_instance.contents["specificClientMessageText"].encode('utf-8'))
            print(f"Sent message to specific client with Player Name: {loaded_msg.original_character_name}")
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