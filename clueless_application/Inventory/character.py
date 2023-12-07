class Character:
    def __init__(self, name=None, location=None):
        self.titleName = ''
        self.location = ''
        self.madeAccusation = False
        self.turn = False
        self.inventory = []
        self.history = []

    def getName(self):
        return self.name