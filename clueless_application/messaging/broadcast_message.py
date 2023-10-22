from messaging.message import Message

class BroadcastMessage(Message):
    type = 'broadcast'
    def __init__(self, type, contents):
        self.contents = contents
   
    # contents props
    # 1. broadcastMessageText

    def printMessage(self):
        print(f"type: {self.type}") 
        print(f"contents:")
        
        for k, v in self.contents.items():
            print(k + ":", v)