from messaging.message import Message

class AccusationMessage(Message):
    type = 'accusation'
    def __init__(self, originalCharacterName, contents):
        self.original_character_name = originalCharacterName
        self.contents = contents

    # Properties
    # type
    # originalCharacterName

    # Contents Properties
    # 1. suspect
    # 2. weapon
    # 3. room 
    # 4. accusationMessageText 

    def printMessage(self):
        print(f"type: {self.type}")
        print(f"originalCharacterName: {self.original_character_name}")
        print(f"contents:")
        
        for k, v in self.contents.items():
            print(k + ": ", v)