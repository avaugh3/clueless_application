class Character:
    def __init__(self,name, location, turn, inventory, history):
        self.name = name
        self.location = location
        self.accusation_avail = False
        self.turn = False
        self.inventory = []
        self.history = []
