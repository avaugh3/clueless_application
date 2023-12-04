class Weapon:
   def __init__(self, name, location):
        self.name = name
        self.location = location

   def updateLocation(self, newLocation):
      self.location = newLocation
      # call update game board