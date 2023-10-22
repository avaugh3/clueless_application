from messaging.message import Message

class SpecificClientMessage(Message):
    type = 'specific_client'
    def __init__(self, originalCharacterName, contents):
        self.original_character_name = originalCharacterName
        self.contents = contents

    # Contents Properties
    # 1. originalCharacterName
    # 2. specificClientMessageText

    def printMessage(self):
        print(f"type: {self.type}") 
        print(f"originalCharacterName: {self.original_character_name}")
        print(f"contents:")
        
        for k, v in self.contents.items():
            print(k + ":", v)