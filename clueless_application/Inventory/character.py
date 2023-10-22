class Character:
    def __init__(self,name, location, turn, inventory, history, madeAccusation):
        self.name = name
        self.location = location
        self.madeAccusation = False
        self.turn = False
        self.inventory = []
        self.history = []
