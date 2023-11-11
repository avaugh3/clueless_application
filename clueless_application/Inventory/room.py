class Room:
   def __init__(self, roomName, location, occupied, occupiedBy):
        self.roomName = roomName
        self.location = location
        self.occupied = occupied
        self.occupiedBy = occupiedBy

   def joinRoom(self, character):
      self.occupied = True
      self.occupiedBy.add(character)
      character.updatelocation(self.location)
      # update Game board 
   
   def leaveRoom(self, character):
      self.occupiedBy.remove(character)
      if occupiedBy.length == 0
         self.occupied = False
      
