class Inventory: 
    def __init__(self, items):
        self.items = items 

    def addItem(self, item):
        self.items = self.items + item

    def getItems(self):
        return self.items 
    
    def shareItem(self, item):
        # not sure how to implement this 
        for values in items: 
            if values == item: 
                print('item in inventory send message to next client')

        if item not in items: print('you do not have this item in your inventory to share. try again')

    
        