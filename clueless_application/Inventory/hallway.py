class Hallway:
   hallwayBetweenStudyAndHallOccupied = False
   hallwayBetweenStudyAndHallOccupiedBy = ''
   hallwayBetweenHallAndLoungeOccupied = False
   hallwayBetweenHallAndLoungeOccupiedBy = ''
   hallwayBetweenConservatoryAndBallroomOccupied = False
   hallwayBetweenConservatoryAndBallroomOccupiedBy = ''

   def __init__(self, location, occupied, occupiedBy):
        self.location = location
        self.occupied = occupied
        self.occupiedBy = occupiedBy