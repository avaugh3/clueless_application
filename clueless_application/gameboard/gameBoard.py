class GameBoard:

    def __init__(self, roomArr, hallwayArr, gameBoardGrid=None):
        self.roomArray = roomArr 
        self.hallwayArray = hallwayArr
        if gameBoardGrid == None:
          self.setGameBoardGrid(self.roomArray, self.hallwayArray)

    def setGameBoardGrid(self, roomArray, hallwayArray, gameboardGridInitiallySetToNone=True):
        if gameboardGridInitiallySetToNone == True:
            self.gameBoardGrid = [
                # row 1
                [roomArray[0], hallwayArray[0], roomArray[1], hallwayArray[1], roomArray[2]],
                # row 2
                [hallwayArray[2], None, hallwayArray[3], None, hallwayArray[4]],
                # row 3
                [roomArray[3], hallwayArray[5], self.roomArray[4], hallwayArray[6], roomArray[5]],
                # row 4 
                [hallwayArray[7], None, hallwayArray[8], None, hallwayArray[9]], 
                # row 5 
                [roomArray[6], hallwayArray[10], roomArray[7], hallwayArray[11], roomArray[8]]
            ]
        else:
           # would set 
           print('Would set a GameBoard grid using the input Room array and Hallway array provided for a given GameBoard object')
    
    def getGameBoardRooms(self):
       return self.roomArray        
    
    def getGameBoardHallways(self):
       return self.hallwayArray

    def getGameBoardGrid(self):
        return self.gameBoardGrid

    def printGameBoardGrid(self):
        if self.gameBoardGrid != None:
            for row in self.gameBoardGrid: 
                for cell in row: 
                    if cell != None:
                        print(cell.getLocation(), end=' ') 
                        print() 
                    else:
                        print("None, void space")
        else:
            print('cannot print gameboard, insufficient input')
      
