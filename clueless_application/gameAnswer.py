import random 
from Inventory.character import Character
from Inventory.room import Room
from Inventory.weapon import Weapon
class GameAnswer: 
    def __init__(self, character=None, weapon=None, room=None):
        self.character = character
        self.weapon = weapon
        self.room = room

        self.weaponsList = ['rope', 'leadpipe', 'knife', 'wrench', 'candlestick', 'revolver', 'dagger']
        self.roomsList = ['study', 'hall', 'lounge', 'diningroom', 'kitchen', 'ballroom', 'conservatory', 'library', 'billardroom']
        self.charactersList = ['missscarlet', 'colonelmustard', 'mrswhite', 'mrgreen', 'mrspeacock', 'professorplum']
     
    
    def GenerateAnswer(self):
        # Create Character option for answer 
        characterChoice = random.randint(0, 5)
        character = self.charactersList[characterChoice]

        # Create room option for answer
        roomChoice = random.randint(0, 8)
        room = self.roomsList[roomChoice]

        # Create weapon option for answer 
        weaponChoice = random.randint(0,5)
        weapon = self.weaponsList[weaponChoice]

        return GameAnswer(character, weapon, room)

    def dealInventory(self):

        # remove the game answer and put in inventory
        charactersLeft = self.charactersList
        charactersLeft.remove(self.character)

        roomsLeft = self.roomsList
        roomsLeft.remove(self.room)

        weaponsLeft = self.weaponsList 
        weaponsLeft.remove(self.weapon)

        return charactersLeft, roomsLeft, weaponsLeft




