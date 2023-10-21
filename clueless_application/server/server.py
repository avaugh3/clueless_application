import sys
import socket
import threading
import pickle
import random 

class CluelessServer:
    
    weapons = ['rope', 'lead pipe', 'knife', 'wrench', 'candlestick', 'revolver']
    rooms = ['study', 'hall', 'lounge', 'dining room', 'kitchen', 'ballroom', 'conservatory', 'library', 'billard room']
    characters = ['miss scarlet', 'colonel mustard', 'mrs. white', 'mr. green', 'mrs. peacock', 'professor plum']
    answerArray = []

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []

    # Function to create the random answer of items. This will be triggered when the user presses the begin game function
    # TODO: Possibly add the division of items out into this function. 
    def createAnswer(self):
        weaponChoice = random.randint(0,5)
        roomChoice = random.randint(0, 8)
        characterChoice = random.randint(0, 5)
        answerArray = [weapons[weaponChoice], rooms[roomChoice], characters[characterChoice]]
        print("A new random answer has been created. The game can now begin")

    # Takes in character trying to move, where they are trying to move to, is it a hallway or room?
    # Character: person making the move
    # location: where they are moving to will either be a Hall object or Room Object
    # isHallway: boolean if this is hallway or not so that can check if is occupied
    def validateMove(self, character, location):
        print("Validating Move")
        if (location.isHallway) {
            if (location.isOccupied){
                # sent to single player
                print("Sorry that hallway is occupied already. Please try again.")
            }
            else{
                # sent to everybody
                print(f"Character {character.name} move is successful to {location.name}")
                character.location = location
                #TODO: Update UI
            }
        }
        else {
            # send to everybody
            print(f"Character {character.name} move is successful to {location.name}")
            character.location = location
            #TODO: Update UI
        }

    
    # Takes in the character making suggesstion, where they currently are located, Weapon and character making a suggesstion.
    # Character: Person making the move
    # location: where the character is located to make suggesstion
    # weaponItem: the weapon they are suggessting 
    # suggesstedCharacter: the character they are suggessting
    def validateSuggestion(self, character, location, weaponItem, suggesstedCharacter):
        print("Validating Suggestion")
        if (character.madeAccusation != true) {
            if (character.location.isRoom == true){
                if weaponItem.name not in weapons: { print('That is not a valid weapon item.') return; } 
                if suggesstedCharacter.name not in characters: { print('That is not a valid character.') return; }
                # send to everybody
                print(f'Player {character.name} has made a valid suggesstion with {suggesstedCharacter.name} in the {location.name} with the {weaponItem.name} ')
                #TODO: Call the disprove for other players to disprove
            }
            else {
                # send to individual
                print("You are not in a room and therefore cannot make a suggestion.")
            }
        }
        else {
            # send to individual
            print("You have made an incorrect accusation before. You cannot make a suggesstion")
        }
    
    def validateAccusation(self, character, room, weapon, suggesstedCharacter):
        print("Validating Accusation")
        if (character.madeAccusation != true) {
            if weapon.name not in weapons: { print('That is not a valid weapon item.') return; } 
            if suggesstedCharacter.name not in characters: { print('That is not a valid character.') return; }
            if room.name not in rooms: { print('That is not a valid room item.') return; } 
            # send to everybody
            print(f'Player {character.name} has made an accusation with {suggesstedCharacter.name} in the {room.name} with the {weapon.name} ')
            # check answer
            if(weapon.name == answerArray[0] & room.name == answerArray[1] & suggesstedCharacter.name == answerArray[2]){
                # send to everybody
                print(f'Congrats! Player {character.name} has correctly made an Accusation and won the game!')
                self.endGame()
            }
            else{
                # send to individual player
                print('Sorry! That is incorrect. Your game is over and you cannot make any more suggesstions/accusations but you can aid your fellow players to disprove suggestions.')
                character.madeAccusation = true
            }
        }
        else {
            # send to individual
            print("You have made an incorrect accusation before. You cannot make another one.")
        }

    # This gets called after someone makes a suggestion and prompts the other players to disprove it. 
    # takes in boolean if can or not disprove, and item
    def validateDisprove(self, canDisprove, item):
        print("Validating Disprove")
        if (canDisprove == true){
            # send this to client who made the suggestion 
            print(f'Hey player! Someone has been able to disprove your suggestion with this item: {item.name}')
        }
        else {
            print("This player cant disprove it. On to the next one")
            #TODO: Send message to next player in list to disprove
        }


    """
    Not sure this functions is needed for this iteration
    def updateGameBoard(self):
        print("Update Game Board")
    """

    def endGame(self):
        print("Winner Determined, Exiting Game")


    """
    Switch-Case to Trigger Methods Based on Message Contents
    """
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
            print("Processing Failed: Unknown Message")
    
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
            self.clients.append(client)

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

                message = data.decode('utf-8')
                print(f"Received: {message}")

                self.processMessage(message)

                response = f"You said: {message}"
                client.send(response.encode('utf-8'))

            except Exception as e:
                print(f"Error: {e}")
                break

        client.close()
        self.clients.remove(client)

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 12345

    server = CluelessServer(HOST, PORT)
    server.start()