import tkinter as tk
from tkinter import *
import os

from Inventory.character import Character
from Inventory.hallway import Hallway
from Inventory.room import Room
# beginning foundation for tkinter game board: stackoverflow

#### Optional Steps to Display the Clue-Less Game Board (stand-alone)  ####
# Pre-requsite: would need to comment out references to certain Clue-Less specific imports
# e.g. (non-exhaustive list ack to account for any future imports) Character|Hallway|Room imports/classes
# -------------------------------------------------------------------------
# 1. Open a terminal window
# 2. Navigate to the clueless_application directory
# 3. Run the gameBoard.py file
#    python3 gameBoard.py

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

    gameBoard={}

    def displayCoordinateForCellClicked(row, column, canvas):
      canvas.itemconfig(gameBoard[(row, column)])

    keyWidth = root.winfo_screenwidth()
    keyHeight = root.winfo_screenheight()

    def getGameBoard():
      # create context for the game board grid
      val = Canvas(root, width=keyWidth, height=keyHeight, bg='#f2d2a9')
      return val

    viewCanvas = getGameBoard()

    def endGame():
        def quitGame():
            print("Clue-Less Game Ended!")
            contextForGameBoard.after(3000,root.destroy())
        quitGame()

    def sendGameBoardToWindow(view):
        print("Sending game board to window")

    # To start the game, display each of the characters
    # ex. to see how 1 character would appear inside of the gameboard, uncomment line 
    def displayCharacters():
        # -- Testing purposes --
        # if uncommented, can see how how it'd look for 1 character
        # to reside in one cell (e.g., hallway between Hall and Lounge)
        # missScarlet.place(x=665, y=140, anchor=NW) 

        missScarlet.place(x=665, y=25, anchor=NW)
        professorPlum.place(x=20, y=262, anchor=NW)
        mrsPeacock.place(x=20, y=480, anchor=NW)
        mrGreen.place(x=380, y=780, anchor=S)
        mrsWhite.place(x=715, y=780, anchor=S)
        colonelMustard.place(x=1052, y=255, anchor=NE)

        # meeting discussion - would want to get cell widths and heights
        # for the cells to determine range of x and y values that would fall 
        # under certain cells which represent particular rooms, hallways, or null spaces

        # -- Testing purposes --
        # if uncommented, can quickly see how it'd look for >1 character
        # to reside in one cell (e.g., same room)
        # professorPlum.place(x=123, y=153, anchor=NW)
        # mrsPeacock.place(x=190, y=153, anchor=NW)

    # Future - tentative
    # param1: the character (as a button) to update the gameBoard's location with  
    # param2: the character's current coordinate (i.e., current location)
    # param3: the character's new coordinate (i.e., new/desired location)
    def updateGameBoard(characterButton, currentCoordinate, newCoordinate):
        print("Updating gameboard...")
        #view.update_idletasks()

    def startGame():
        global gameBoard
        print("Clue-Less Game Started!")
        contextForGameBoard.pack_forget()

        # -- Testing purposes --
        # if uncommented, a Character instantiation for Miss Scarlet would occur 
        #  missScarletChar = Character('Miss  Scarlet')

        # Rooms created (9)
        study = Room('Study', {0,0}, False, 'N/A')
        hall = Room('Hall', {0,2}, False, 'N/A')
        lounge = Room('Lounge', {0,4}, False, 'N/A')
        library = Room('Library', {2,0}, False, 'N/A')
        billiardRoom = Room('Billiard Room', {2,2}, False, 'N/A')
        diningRoom = Room('Dining Room', {2,4}, False, 'N/A')
        conservatory = Room('Conservatory', {4,0}, False, 'N/A')
        ballroom = Room('Ballroom', {4,2}, False, 'N/A')
        kitchen = Room('Kitchen', {4,4}, False, 'N/A')

        # Hallways created (12)
        studyHallHallway = Hallway({0,1}, False, 'N/A')
        hallLoungeHallway = Hallway({0,3}, False, '')
        studyLibraryHallway = Hallway({1,0}, False, 'N/A')
        hallBilliardRoomHallway = Hallway({1,2}, False, 'N/A')
        loungeDiningRoomHallway = Hallway({1,4}, False, 'N/A')
        libraryBilliardRoomHallway = Hallway({2,1}, False, 'N/A')
        billiardRoomDiningRoomHallway = Hallway({2,3}, False, 'N/A')
        libraryConservatoryHallway = Hallway({3,0}, False, 'N/A')
        billiardBallroomHallway = Hallway({3,2}, False, 'N/A')
        diningRoomKitchenHallway = Hallway({3,4}, False, 'N/A')
        conservatoryBallroomHallway = Hallway({4,1}, False, 'N/A')
        ballroomKitchenHallway = Hallway({4,3}, False, 'N/A')

        # -- Testing purposes --
        # if uncommented and Miss Scarlet moved to the hallway between the Hall and Lounge
        #   hallLoungeHallway.isOccupied would be updated to True 
        #   hallLoungeHallway.occupiedBy would be updated to the character's name (Miss Scarlet in this case)
        # hallLoungeHallway.isOccupied = True
        # hallLoungeHallway.occupiedBy = missScarletChar.getName()

        # set up the view of the game board
        def printGameBoard(view):
            gameBoard={}
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
                        gameBoard[(row,col)]=rect

                    elif (row == 0 and col == 2):
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'medium seagreen')

                        view.create_text(420, 20, text='Hall', font=("Courier bold", 12), fill='black')
                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoard[(row,col)]=rect

                    elif (row == 0 and col == 4):
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'medium seagreen')

                        view.create_text(750, 20, text='Lounge', font=("Courier bold", 12), fill='black')
                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoard[(row,col)]=rect

                    elif (row == 2 and col == 0):
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'medium seagreen')

                        view.create_text(75, 235, text='Library', font=("Courier bold", 12), fill='black')
                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoard[(row,col)]=rect

                    elif (row == 2 and col == 2):
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'medium seagreen')

                        view.create_text(420, 235, text='Billiard Room', font=("Courier bold", 12), fill='black')
                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoard[(row,col)]=rect

                    elif (row == 2 and col == 4):
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'medium seagreen')

                        view.create_text(750, 235, text='Dining Room', font=("Courier bold", 12), fill='black')
                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoard[(row,col)]=rect

                    elif (row == 4 and col == 0):
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'medium seagreen')

                        view.create_text(75, 460, text='Conservatory', font=("Courier bold", 12), fill='black')
                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoard[(row,col)]=rect

                    elif (row == 4 and col == 2):
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'medium seagreen')

                        view.create_text(420, 460, text='Ballroom', font=("Courier bold", 12), fill='black')
                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoard[(row,col)]=rect

                    elif (row == 4 and col == 4):
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'medium seagreen')

                        view.create_text(750, 460, text='Kitchen', font=("Courier bold", 12), fill='black')
                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoard[(row,col)]=rect

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
                            gameBoard[(row,col)]=rect

                    else: 
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'grey')

                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoard[(row,col)]=rect
            return gameBoard
        
        viewCanvas.pack(side=TOP, fill=BOTH, padx=120, pady=120)
        print(viewCanvas.gettags(CURRENT))
        viewCanvas.itemconfig(CURRENT, fill="LightSalmon3")

        displayCharacters()

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
        gameBoard = printGameBoard(viewCanvas)
    
    contextForGameBoard = GameBoardContext(root)
    contextForGameBoard.config(bg='#f2d2a9')

    endGameButton=Button(contextForGameBoard, text='End Game',command=endGame)
    endGameButton.place(x=950, y=600, anchor=E)
    endGameButton.config(bg='#78a8bc', fg ='white')

    startNewGameButton=Button(contextForGameBoard, text='Start New Game', command=startGame)
    startNewGameButton.place(x=850, y=600, anchor=E)
    startNewGameButton.config(bg='#78a8bc', fg='white')

    clueLessSplashScreenButton=Button(contextForGameBoard, text='Splash Screen')
    splashScreenPhoto=PhotoImage(file='clueless-splash-screen-image.png')
    clueLessSplashScreenButton.config(image=splashScreenPhoto, width='575', height='500')
    clueLessSplashScreenButton.place(x=100, y=115, anchor=NW)

    # temp testing to show Miss Scarlet in the hallway between the Hall and Lounge
    missScarlet=Button(root, text='miss scarlet')
    missScarletPhoto=PhotoImage(file='miss-scarlet-with-name.png')
    missScarlet.config(image=missScarletPhoto, width='70', height='70')
    missScarlet.place_forget()

    professorPlum=Button(root, text='professor plum')
    professorPlumPhoto=PhotoImage(file='professor-plum-with-name.png')
    professorPlum.config(image=professorPlumPhoto, width='70', height='70')
    professorPlum.place_forget()

    mrsPeacock=Button(root, text='mrs. peacock')
    mrsPeacockPhoto=PhotoImage(file='mrs-peacock-with-name.png')
    mrsPeacock.config(image=mrsPeacockPhoto, width='70', height='70')
    mrsPeacock.place_forget()

    mrGreen=Button(root, text='mr. green')
    mrGreenPhoto=PhotoImage(file='mr-green-with-name.png')
    mrGreen.config(image=mrGreenPhoto, width='70', height='70')
    mrGreen.place_forget()

    mrsWhite=Button(root, text='mrs. white')
    mrsWhitePhoto=PhotoImage(file='mrs-white-with-name.png')
    mrsWhite.config(image=mrsWhitePhoto, width='70', height='70')
    mrsWhite.place_forget()

    colonelMustard=Button(root, text='colonel mustard')
    colonelMustardPhoto=PhotoImage(file='col-mustard-with-name.png')
    colonelMustard.config(image=colonelMustardPhoto, width='70', height='70')
    colonelMustard.place_forget()

    clueLessNameForFrame = Label(root, text='Clue-Less', font=('Arial 20 bold'))
    clueLessNameForFrame.config(bg='#f2d2a9', fg='#000C66')
    clueLessNameForFrame.place(x=80, y=30, anchor=CENTER)

    root.mainloop()