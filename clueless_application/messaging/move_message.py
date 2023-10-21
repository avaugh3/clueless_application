from messaging.message import Message

class MoveMessage(Message):
    type = 'move'
    def __init__(self, contents):
        self.contents = contents 

    # contents prop
    # 1. direction   

    def printMessage(self):
        print(f"type: {self.type}") 
        print(f"contents:")
        
        for k, v in self.contents.items():
            print(k + ":", v)