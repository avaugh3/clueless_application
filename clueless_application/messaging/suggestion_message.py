from messaging.message import Message

class SuggestionMessage(Message):
    type = 'suggestion'
    def __init__(self, contents):
        self.contents = contents

    # contents props
    # 1. suspect
    # 2. weapon
    # 3. suggestionMessageText 
    #
    # note: room is not included because the server will determine the room based on its knowledge of the character's position on 
    # the game board 

    def printMessage(self):
        print(f"type: {self.type}") 
        print(f"contents:")
        
        for k, v in self.contents.items():
            print(k + ":", v)
    