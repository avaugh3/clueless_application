class Room:
   def __init__(self, roomName, location, occupied, occupiedBy):
      self.roomName = roomName
      self.location = location
      self.occupied = occupied
      self.occupiedBy = occupiedBy

   def getName(self):
      return self.roomName
   
   def getLocation(self):
      return self.location
   
   def isOccupied(self):
      return self.occupied
   
   def isOccupiedBy(self):
      # -- Testing purposes --
      # if uncommented can confirm that a character, by name is occupying a given room
      # self.occupiedBy = 'Miss Scarlet'
      return self.occupiedBy

   def joinRoom(self, character):
      self.occupied = True
      self.occupiedBy.add(character)
      character.updatelocation(self.location)
      # update Game board 
   
   def leaveRoom(self, character):
      self.occupiedBy.remove(character)
      if (self.occupiedBy.length == 0):
         self.occupied = False  
