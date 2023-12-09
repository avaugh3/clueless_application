class Hallway:
   def __init__(self, location, occupied, occupiedBy):
        self.location = location
        self.occupied = occupied
        self.occupiedBy = occupiedBy
   
   def moveIntoHallway(self, Character):
      if self.occupied:
         print('Sorry! This hallway is already occupied')
      else:
         self.occupied = True
         self.occupiedBy = Character

   def moveOutOfHallway(self):
      self.occupied = False
      self.occupiedBy = ''
