from messaging.message import Message

class SpecificClientMessage(Message):
    type = 'specific_client'
    def __init__(self, contents):
        self.contents = contents

    # contents props
    # 1. specificClientMessageText

    def printMessage(self):
        print(f"type: {self.type}") 
        print(f"contents:")
        
        for k, v in self.contents.items():
            print(k + ":", v)