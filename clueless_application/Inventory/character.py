class Character:

    def __init__(self, name=None, location=None):
        self.name = name
        self.location = location
        self.madeAccusation = False
        self.turn = False
        self.inventory = []
        self.history = []

    def getName(self):
        return self.name