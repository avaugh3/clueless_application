import socket
import threading
import pickle
from collections import OrderedDict
from messaging.message import Message

class CluelessServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = OrderedDict()

    def validateMove(self):
        print("Validating Move")
    
    def validateSuggestion(self):
        print("Validating Suggestion")
    
    def validateAccusation(self):
        print("Validating Accusation")

    def validateDisprove(self):
        print("Validating Disprove")

    def updateGameBoard(self):
        print("Update Game Board")

    def determineGameWinner(self):
        print("Determining if Their is a Game Winner")
    
    def endGame(self):
        print("Winner Determined, Exiting Game")

    """
    Switch-Case to Trigger Methods Based on Message Contents
    """
    def processMessage(self, message, client):
        loaded_msg = pickle.loads(message)
        print(f"Processing Message from Client {self.clients[client]}: {loaded_msg.contents}")

        if loaded_msg.type == 'move':
            self.validateMove()
        elif loaded_msg.type == 'suggestion':
            self.validateSuggestion()
        elif loaded_msg.type == 'accusation':
            self.validateAccusation()
        elif loaded_msg.type == 'disprove':
            self.validateDisprove()
        else:
            print(f"Processing Failed: Unknown Message Type \"{loaded_msg.type}\"")
    
    """
    Starts Server Listening for Client Connections
    """
    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
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