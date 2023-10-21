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
        #print(f"Processing Message from Client {self.clients[client]}: {loaded_msg.contents}")
        print(f"Processing Message from Client {self.clients[client]}: {'type:', loaded_msg.type, 'contents:', loaded_msg.contents}")

        if loaded_msg.type == 'move':
            # create a MoveMessage object  
            self.validateMove()
            #self.broadcastMessage
        elif loaded_msg.type == 'suggestion':
            """
            Method needed to get the client's current room 
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
        self.log.info('Broadcasting message: %s', message)
        for c in clients:
            c.send(message)
            
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

            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()
    
    """
    When Client Sends Message, New Thread is Opened to Process the Message
    """
    def handle_client(self, client):
        while True:
            try:
                data = client.recv(1024)
                if not data:
                    break

                self.processMessage(data, client)
                #self.broadcastMessage(clients, data)

                response = f"Message Received by Server {self.host}:{self.port}"
                client.send(response.encode('utf-8'))

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