class Character:
    name = 'Megan Rutch'
    location = ''
    madeAccusation = False
    turn = False
    inventory = []
    history = []

    def __init__(self, name, location):
        self.titleName = titleName
        self.location = location
        self.madeAccusation = False
        self.turn = False
        self.inventory = []
        self.history = []

    def getName(self):
        return self.name