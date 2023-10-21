class Message:
    def __init__(self, type, contents):
        self.type = type
        self.contents = contents
        
    def printMessage(self):
        print(f"type: {self.type}") 
        print(f"contents:")
        
        for k, v in self.contents.items():
            print(k + ":", v)