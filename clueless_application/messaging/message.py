class Message:
    def __init__(self, type, originalCharacterName=None, contents=None):
        self.type = type
        self.originalCharacterName = originalCharacterName
        self.contents = contents
        
    def printMessage(self):
        print(f"type: {self.type}") 
        print(f"originalCharacterName: {self.originalCharacterName }")
        print(f"contents:")
        
        for k, v in self.contents.items():
            print(k + ":", v)