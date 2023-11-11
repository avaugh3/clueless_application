import random 
from Inventory.character import Character
from Inventory.room import Room
from Inventory.weapon import Weapon
class GameAnswer: 
    weaponsList = ['rope', 'lead pipe', 'knife', 'wrench', 'candlestick', 'revolver']
    roomsList = ['study', 'hall', 'lounge', 'dining room', 'kitchen', 'ballroom', 'conservatory', 'library', 'billard room']
    charactersList = ['miss scarlet', 'colonel mustard', 'mrs. white', 'mr. green', 'mrs. peacock', 'professor plum']

    def __init__(self, character, weapon, room):
        self.character = character
        self.weapon = weapon
        self.room = room
     
    
    def GenerateAnswer(self):
        weaponsList = ['rope', 'lead pipe', 'knife', 'wrench', 'candlestick', 'revolver']
        roomsList = ['study', 'hall', 'lounge', 'dining room', 'kitchen', 'ballroom', 'conservatory', 'library', 'billard room']
        charactersList = ['miss scarlet', 'colonel mustard', 'mrs. white', 'mr. green', 'mrs. peacock', 'professor plum']
        # Create Character option for answer 
        characterChoice = random.randint(0, 5)
        character = Character(charactersList[characterChoice], None, None, [], [], False)

        # Create room option for answer
        roomChoice = random.randint(0, 8)
        room = Room(roomsList[roomChoice], None, None, None)

        # Create weapon option for answer 
        weaponChoice = random.randint(0,5)
        weapon = Weapon(weaponsList[weaponChoice], None)

        return GameAnswer(character, weapon, room)

    def dealInventory(self):
        weaponsList = ['rope', 'lead pipe', 'knife', 'wrench', 'candlestick', 'revolver']
        roomsList = ['study', 'hall', 'lounge', 'dining room', 'kitchen', 'ballroom', 'conservatory', 'library', 'billard room']
        charactersList = ['miss scarlet', 'colonel mustard', 'mrs. white', 'mr. green', 'mrs. peacock', 'professor plum']
        resultingInventory = []

        # remove the game answer and put in inventory
        charactersLeft = charactersList
        charactersLeft.remove(self.character.name)
        resultingInventory = resultingInventory + charactersLeft

        roomsLeft = roomsList
        roomsLeft.remove(self.room.roomName)
        resultingInventory = resultingInventory + roomsLeft

        weaponsLeft = weaponsList 
        weaponsLeft.remove(self.weapon.name)
        resultingInventory = resultingInventory + weaponsLeft

        random.shuffle(resultingInventory)
        return resultingInventory




