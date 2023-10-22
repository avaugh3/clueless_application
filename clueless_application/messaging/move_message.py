from messaging.message import Message

class MoveMessage(Message):
    type = 'move'
    def __init__(self, originalCharacterName, contents):
        self.original_character_name = originalCharacterName
        self.contents = contents 

    # Properties
    # type
    # originalCharacterName

    # Contents Properties
    # 1. direction 

    def printMessage(self):
        print(f"type: {self.type}") 
        print(f"originalCharacterName: {self.original_character_name}")
        print(f"contents:")
        
        for k, v in self.contents.items():
            print(k + ":", v)