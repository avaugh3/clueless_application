import socket
import pickle
from messaging.message import Message

class CluelessClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.host, self.port))
        print(f"Connected to {self.host}:{self.port}")

    def send_message(self, message):
        
        pickled_msg = pickle.dumps(client_msg)
        
        self.socket.send(pickled_msg)
        response = self.socket.recv(1024).decode('utf-8')
        
        #Server Response
        print(response)

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
        message = input("Enter a message (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break

        client_msg = Message(message, f"Testing message type {message}")

        client.send_message(client_msg)

    client.close()