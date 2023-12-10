import tkinter as tk
from tkinter import *
import os

from Inventory.character import Character
from Inventory.hallway import Hallway
from Inventory.room import Room
from gameboard.gameBoard import GameBoard 

# beginning foundation for tkinter game board: stackoverflow

#### Optional Steps to Display the Clue-Less Game Board (stand-alone)  ####
# Pre-requsite: would need to comment out references to certain Clue-Less specific imports
# e.g. (non-exhaustive list ack to account for any future imports) Character|Hallway|Room imports/classes
# -------------------------------------------------------------------------
# 1. Open a terminal window
# 2. Navigate to the clueless_application directory
# 3. Run the gameBoardContext.py file
#    python3 gameBoardContext.py

# Set up foundational context frame in which the game board grid sits 
class GameBoardContext(Frame):
    def __init__(self, master, width=0.7, height=0.52):
        Frame.__init__(self, master)
        
        self.pack(side=TOP, fill=BOTH, expand=YES)

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        the_width = screen_width*width
        the_height = screen_width*height

        x = (screen_width/2) - (the_width/2)
        y = (screen_height/2) - (the_height/2)
        self.master.geometry('%dx%d+%d+%d' % (the_width, the_height, x, y))

if __name__ == '__main__':
    root = tk.Tk()
    root.configure(background='#f2d2a9')

    root.title("Clue-Less Application Game Board")

    # Rooms (9)
    study = Room('study', (0,0), False, 'N/A')
    hall = Room('hall', (0,2), False, 'N/A')
    lounge = Room('lounge', (0,4), False, 'N/A')
    library = Room('library', (2,0), False, 'N/A')
    billiardRoom = Room('billiardroom', (2,2), False, 'N/A')
    diningRoom = Room('diningroom', (2,4), False, 'N/A')
    conservatory = Room('conservatory', (4,0), False, 'N/A')
    ballroom = Room('ballroom', (4,2), False, 'N/A')
    kitchen = Room('kitchen', (4,4), False, 'N/A')

    roomArray = [study, hall, lounge, library, billiardRoom, diningRoom, conservatory, ballroom, kitchen]

    # Hallways (12)
    studyHallHallway = Hallway((0,1), False, 'N/A')
    hallLoungeHallway = Hallway((0,3), False, 'N/A')
    studyLibraryHallway = Hallway((1,0), False, 'N/A')
    hallBilliardRoomHallway = Hallway((1,2), False, 'N/A')
    loungeDiningRoomHallway = Hallway((1,4), False, 'N/A')
    libraryBilliardRoomHallway = Hallway((2,1), False, 'N/A')
    billiardRoomDiningRoomHallway = Hallway((2,3), False, 'N/A')
    libraryConservatoryHallway = Hallway((3,0), False, 'N/A')
    billiardRoomBallroomHallway = Hallway((3,2), False, 'N/A')
    diningRoomKitchenHallway = Hallway((3,4), False, 'N/A')
    conservatoryBallroomHallway = Hallway((4,1), False, 'N/A')
    ballroomKitchenHallway = Hallway((4,3), False, 'N/A')

    hallwayArray = [studyHallHallway, hallLoungeHallway, studyLibraryHallway, hallBilliardRoomHallway, loungeDiningRoomHallway, 
        libraryBilliardRoomHallway, billiardRoomDiningRoomHallway, libraryConservatoryHallway,billiardRoomBallroomHallway, 
        diningRoomKitchenHallway, conservatoryBallroomHallway, ballroomKitchenHallway]

    gameBoardGridGui={}

    def displayCoordinateForCellClicked(row, column, canvas):
      canvas.itemconfig(gameBoardGridGui[(row, column)])

    keyWidth = root.winfo_screenwidth()
    keyHeight = root.winfo_screenheight()

    def getgameBoardGridGui():
      # create context for the game board grid
      val = Canvas(root, width=keyWidth, height=keyHeight, bg='#f2d2a9')
      return val

    viewCanvas = getgameBoardGridGui()

    def endGame():
        def quitGame():
            print("Clue-Less Game Ended!")
            contextForGameBoard.after(3000,root.destroy())
        quitGame()

    def sendGameBoardToWindow(view):
        print("Sending game board to window")

    # To start the game, display each of the characters
    # ex. to see how 1 character would appear inside of the gameboard, uncomment line 
    def displayCharacters(missScarletB, professorPlumB, mrsPeacockB, mrGreenB, mrsWhiteB, colonelMustardB):
        # -- Testing purposes --
        # if uncommented, can see how how it'd look for 1 character
        # to reside in one cell (e.g., hallway between Hall and Lounge)
        # missScarletB.place(x=665, y=140, anchor=NW) 
        missScarletB.place(x=665, y=25, anchor=NW)
        professorPlumB.place(x=20, y=262, anchor=NW)
        mrsPeacockB.place(x=20, y=480, anchor=NW)
        mrGreenB.place(x=380, y=780, anchor=S)
        mrsWhiteB.place(x=715, y=780, anchor=S)
        colonelMustardB.place(x=1052, y=255, anchor=NE)

        # -- Testing purposes --
        # if uncommented, can quickly see how it'd look for >1 character
        # to reside in one cell (e.g., same room)
        # professorPlum.place(x=123, y=153, anchor=NW)
        # mrsPeacock.place(x=190, y=153, anchor=NW)

    def updateGameBoardGridGui(charButton, currentLocationGui=(), newLocationGui=()):
        # checking that a move can be made using a board update
        # expected validation that would occur
        # ex valid move checks
        # - if first move, trying to move to a location that is not a Hallway adjacent to starting block (i.e., home square)
        # - not trying to go into a void gray space (neither Room nor Hallway)
        # - not trying to go into a Hallway that is already occupied 
        # - not trying to take a secret passageway from a room that doesn't have a secret passageway (info board to handle)
        # ex other update happening 
        # - updating Character info (e.g., the character's location)
        charButton.place(x=newLocationGui[0], y=newLocationGui[1])

    def startGame():
        global gameBoardGridGui
        print("Clue-Less Game Started!")
        contextForGameBoard.pack_forget() 

        # -- Testing purposes --
        # if uncommented, a Character instantiation for Miss Scarlet would occur 
        #  missScarletCharacter = Character('Miss  Scarlet')

        gameBoard = GameBoard(roomArray, hallwayArray)
        # get grid alone
        gameBoardGrid = gameBoard.getGameBoardGrid()
        # could also maintain access to grid via the gameBoard instance obj
        # gameBoard.gameBoardGrid[row][col]

        # -- Testing purposes --
        # if uncommented can confirm that for the game board instance's grid, accessing a particular cell 
        # as expected for its position gives the expected name 
        # in this case 0,0 in the game board grid should be a room with the name of Study 
        # Study room key info from 5 x 5 game board grid below
        # val = gameBoard.getGameBoardGrid() 
        # print(gameBoard.gameBoardGrid[0][0].getName())
        # print(gameBoard.gameBoardGrid[0][4].getName())
        # print(gameBoard.gameBoardGrid[0][0].getLocation())
        # print(gameBoard.gameBoardGrid[0][0].isOccupied()) 
        # For line below, should also uncomment testing purposes line in Room's isOccupiedBy method
        # print('Room ' + (gameBoard.gameBoardGrid[0][0].getName() + ' is occupied by ' + gameBoard.gameBoardGrid[0][0].isOccupiedBy()))
        gameBoard.printGameBoardGrid()
        
        # set up the view of the game board
        def printgameBoardGridGui(view):
            gameBoardGridGui={}
            width_to_use=view.winfo_width()
            height_to_use=view.winfo_height()

            gridWidth = width_to_use/5
            gridHeight = height_to_use/5

            # row as 0 to keep top left game board pos as 0,0
            rowNumber = -1
            for row in range(5):
                # col as 0 to keep top left game board pos as 0,0
                columnNumber = -1
                rowNumber = rowNumber + 1
            
                for col in range(5):
                    if (row == 0 and col == 0):
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'medium seagreen')

                        view.create_text(75, 20, text='Study', font=("Courier bold", 12), fill='black')

                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoardGridGui[(row,col)]=rect

                    elif (row == 0 and col == 2):
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'medium seagreen')

                        view.create_text(420, 20, text='Hall', font=("Courier bold", 12), fill='black')
                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoardGridGui[(row,col)]=rect

                    elif (row == 0 and col == 4):
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'medium seagreen')

                        view.create_text(750, 20, text='Lounge', font=("Courier bold", 12), fill='black')
                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoardGridGui[(row,col)]=rect

                    elif (row == 2 and col == 0):
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'medium seagreen')

                        view.create_text(75, 235, text='Library', font=("Courier bold", 12), fill='black')
                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoardGridGui[(row,col)]=rect

                    elif (row == 2 and col == 2):
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'medium seagreen')

                        view.create_text(420, 235, text='Billiard Room', font=("Courier bold", 12), fill='black')
                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoardGridGui[(row,col)]=rect

                    elif (row == 2 and col == 4):
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'medium seagreen')

                        view.create_text(750, 235, text='Dining Room', font=("Courier bold", 12), fill='black')
                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoardGridGui[(row,col)]=rect

                    elif (row == 4 and col == 0):
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'medium seagreen')

                        view.create_text(75, 460, text='Conservatory', font=("Courier bold", 12), fill='black')
                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoardGridGui[(row,col)]=rect

                    elif (row == 4 and col == 2):
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'medium seagreen')

                        view.create_text(420, 460, text='Ballroom', font=("Courier bold", 12), fill='black')
                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoardGridGui[(row,col)]=rect

                    elif (row == 4 and col == 4):
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'medium seagreen')

                        view.create_text(750, 460, text='Kitchen', font=("Courier bold", 12), fill='black')
                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoardGridGui[(row,col)]=rect

                    elif ((row == 0 and col == 1) or (row == 0 and col == 3) or (row == 1 and col ==0) or (row == 1 and col == 2) or (row == 2 and col == 3) or (row == 3 and col == 0) or (row == 3 and col == 2) or (row == 3 and col == 4) or (row == 2 and col == 1)
                        or (row == 2 and col == 3) or (row == 1 and col == 2) or (row == 1 and col == 4) or (row == 4 and col == 1) or (row == 4 and col == 3)):
                            columnNumber = columnNumber + 1
                            rect = view.create_rectangle(col * gridWidth,
                            row * gridHeight,
                            (col + 1) * gridWidth,
                            (row + 1) * gridHeight,
                            fill = 'LightSalmon3')

                            view.create_text(685, 545, font=("Courier bold", 12), fill='black')
                            view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                            gameBoardGridGui[(row,col)]=rect

                    else: 
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'grey')

                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoardGridGui[(row,col)]=rect
            return gameBoardGridGui
        
        viewCanvas.pack(side=TOP, fill=BOTH, padx=120, pady=120)
        print(viewCanvas.gettags(CURRENT))
        viewCanvas.itemconfig(CURRENT, fill="LightSalmon3")

        displayCharacters(missScarletButton, professorPlumButton, mrsPeacockButton, mrGreenButton, mrsWhiteButton, colonelMustardButton)

        exit_button = Button(root, text="Exit Game", bg="red", fg="white", command=endGame) 
        exit_button.place(x=985, y=134) 

        secret_passageway_study_button = Button(root, text="S", bg="DarkOrchid3", fg="white") 
        secret_passageway_study_button.place(x=266, y=202) 

        secret_passageway_lounge_button = Button(root, text="S", bg="DarkOrchid3", fg="white") 
        secret_passageway_lounge_button.place(x=931, y=202)

        secret_passageway_conservatory_button = Button(root, text="S", bg="DarkOrchid3", fg="white") 
        secret_passageway_conservatory_button.place(x=266, y=572) 

        secret_passageway_kitchen_button = Button(root, text="S", bg="DarkOrchid3", fg="white") 
        secret_passageway_kitchen_button.place(x=931, y=572) 

        root.update_idletasks()

        def clickOnGameBoard(event):
          if viewCanvas.find_withtag(CURRENT):
            print(viewCanvas.gettags(CURRENT))
            viewCanvas.update_idletasks()

        #bind an event when you click on the game board
        viewCanvas.bind("<Button-1>", clickOnGameBoard)

        root.update_idletasks()

        #show the gameboard in the Canvas
        gameBoardGridGui = printgameBoardGridGui(viewCanvas)
        
        # -- Testing purposes (updating a character's position on GUI game board) --
        # if uncommented, would move Miss Scarlet from her starting block position into 
        # the Hallway between the Hall and Lounge
        #missScarletCharacter = Character("missscarlet")
        #charDict = {missScarletCharacter.name : missScarletButton}

        #theCurrentLocationX = missScarletButton.winfo_rootx()-238 
        #theCurrentLocationY = missScarletButton.winfo_rooty()-63

        #currentLocation = (theCurrentLocationX, theCurrentLocationY)
        #newLocation = (theCurrentLocationX, theCurrentLocationY+115)
        
        #updateGameBoardGridGui(charDict.get('missscarlet'), currentLocation, newLocation)
    
    contextForGameBoard = GameBoardContext(root)
    contextForGameBoard.config(bg='#f2d2a9')

    endGameButton=Button(contextForGameBoard, text='End Game', command=endGame)
    endGameButton.place(x=950, y=600, anchor=E)
    endGameButton.config(bg='#78a8bc', fg ='white')

    startNewGameButton=Button(contextForGameBoard, text='Start New Game', command=startGame)
    startNewGameButton.place(x=850, y=600, anchor=E)
    startNewGameButton.config(bg='#78a8bc', fg='white')

    clueLessSplashScreenButton=Button(contextForGameBoard, text='Splash Screen')
    splashScreenPhoto=PhotoImage(file='clueless-splash-screen-image.png')
    clueLessSplashScreenButton.config(image=splashScreenPhoto, width='575', height='500')
    clueLessSplashScreenButton.place(x=100, y=115, anchor=NW)

    missScarletButton=Button(root, text='missscarlet')
    missScarletPhoto=PhotoImage(file='miss-scarlet-with-name.png')
    missScarletButton.config(image=missScarletPhoto, width='70', height='70')
    missScarletButton.place_forget()

    professorPlumButton=Button(root, text='professorplum')
    professorPlumPhoto=PhotoImage(file='professor-plum-with-name.png')
    professorPlumButton.config(image=professorPlumPhoto, width='70', height='70')
    professorPlumButton.place_forget()

    mrsPeacockButton=Button(root, text='mrspeacock')
    mrsPeacockPhoto=PhotoImage(file='mrs-peacock-with-name.png')
    mrsPeacockButton.config(image=mrsPeacockPhoto, width='70', height='70')
    mrsPeacockButton.place_forget()

    mrGreenButton=Button(root, text='mrgreen')
    mrGreenPhoto=PhotoImage(file='mr-green-with-name.png')
    mrGreenButton.config(image=mrGreenPhoto, width='70', height='70')
    mrGreenButton.place_forget()

    mrsWhiteButton=Button(root, text='mrswhite')
    mrsWhitePhoto=PhotoImage(file='mrs-white-with-name.png')
    mrsWhiteButton.config(image=mrsWhitePhoto, width='70', height='70')
    mrsWhiteButton.place_forget()

    colonelMustardButton=Button(root, text='colonelmustard')
    colonelMustardPhoto=PhotoImage(file='col-mustard-with-name.png')
    colonelMustardButton.config(image=colonelMustardPhoto, width='70', height='70')
    colonelMustardButton.place_forget()

    clueLessNameForFrame = Label(root, text='Clue-Less', font=('Arial 20 bold'))
    clueLessNameForFrame.config(bg='#f2d2a9', fg='#000C66')
    clueLessNameForFrame.place(x=80, y=30, anchor=CENTER)

    root.mainloop()