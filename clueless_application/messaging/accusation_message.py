from messaging.message import Message

class AccusationMessage(Message):
    type = 'accusation'
    def __init__(self, contents):
        self.contents = contents

    # contents props
    # 1. suspect
    # 2. weapon
    # 3. room 
    # 4. accusationMessageText 

    def printMessage(self):
        print(f"type: {self.type}, contents: \n")
        
        for k, v in self.contents.items():
            print(k + ": ", v)