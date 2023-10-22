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

if __name__ == "__main__":
    #HOST = '127.0.0.1'
    #PORT = 12345

    HOST = input("Enter Server IP Address: ")
    PORT = int(input("Enter Server Port: "))

    client = CluelessClient(HOST, PORT)
    client.connect()

    while True:
        message = input("Enter a message (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break

        client_msg = Message(message, f"Testing message type {message}")

        client.send_message(client_msg)

    client.close()