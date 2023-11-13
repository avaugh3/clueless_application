class Character:
    def __init__(self, name, location, turn, inventory, history, madeAccusation):
        self.name = name
        self.location = location
        self.madeAccusation = False
        self.turn = False
        self.inventory = []
        self.history = []

    @staticmethod
    def characterSymbolLookup(characterName):
        if characterName == 'miss scarlet':
            return '!'
        elif characterName == 'colonel mustard':
            return '$'
        elif characterName == 'missus white':
            return '*'
        elif characterName == 'mister green':
            return '^'
        elif characterName == 'missus peacock':
            return '@'
        elif characterName == 'professor plum':
            return '&'
