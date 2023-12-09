import tkinter as tk
from tkinter import *
import os

from Inventory.character import Character
from Inventory.hallway import Hallway
from Inventory.room import Room
# beginning foundation for tkinter game board: stackoverflow

#### Steps to Display the Clue-Less Game Board (stand-alone)  ####
# 1. Open a terminal window
# 2. Navigate to the clueless_application directory
# 3. Run the gameBoard.py file
#    python3 gameBoard.py

# Set up foundational context frame in which the game board grid sits 
class GameBoardContext(Frame):
    def __init__(self, master, width=0.65, height=0.48):
        Frame.__init__(self, master)
        
        self.pack(side=TOP, fill=BOTH, expand=YES)

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        the_width = screen_width*width
        the_height = screen_width*height

        x = (screen_width/2) - (the_width/2)
        y = (screen_height/2) - (the_height/2)
        self.master.geometry('%dx%d+%d+%d' % (the_width, the_height, x, y))

        self.master.overrideredirect(True)
        self.lift()

if __name__ == '__main__':
    root = tk.Tk()
    root.configure(background='#f2d2a9')

    gameBoard={}

    def displayCoordinateForCellClicked(row, column, canvas):
      canvas.itemconfig(gameBoard[(row, column)])

    keyWidth = root.winfo_screenwidth()
    keyHeight = root.winfo_screenheight()

    def getGameBoard():
      #create context for the game board grid
      val = Canvas(root, width=keyWidth, height=keyHeight, bg='#f2d2a9')
      return val

    viewCanvas = getGameBoard()

    # Future: should also make it known which secret passage - based on param2, should be able to get room's coordinates
    # param1: characterName (i.e. room of starting pos)
    # param2: roomNameOfSecretPassageway or a roomObj (can likely pass this in, will know the name based on the 
    # secretPassageway button)
    def takeSecretPassageway():
        print("take a secret passageway")

    def endGame():
        def quitGame():
            print("Clue-Less Game Ended!")
            contextForGameBoard.after(3000,root.destroy())
        quitGame()

    def sendGameBoardToWindow(view):
        print("Sending game board to window")

    # To start the game, display each of the characters
    def displayCharacters():
        missScarlet.place(x=610, y=135, anchor=NW)
        professorPlum.place(x=20, y=240, anchor=NW)
        mrsPeacock.place(x=20, y=435, anchor=NW)
        mrGreen.place(x=340, y=720, anchor=S)
        mrsWhite.place(x=640, y=720, anchor=S)
        colonelMustard.place(x =975, y=240, anchor=NE)

    # Future - tentative
    # param1: gameBoard to update
    # param2: the character to update the gameBoard with 
    # param3: the character's newLocation
    def updateGameBoard(view, characterObj, newLocation):
        print("Sending game board to window")
        #view.update_idletasks()

    def startGame():
        global gameBoard
        print("Clue-Less Game Started!")
        contextForGameBoard.pack_forget()

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

                        view.create_text(75, 60, text='Study', font=("Courier bold", 16), fill='black')

                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoard[(row,col)]=rect

                    elif (row == 0 and col == 2):
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'medium seagreen')

                        view.create_text(380, 65, text='Hall', font=("Courier bold", 16), fill='black')
                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoard[(row,col)]=rect

                    elif (row == 0 and col == 4):
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'medium seagreen')

                        view.create_text(685, 65, text='Lounge', font=("Courier bold", 16), fill='black')
                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoard[(row,col)]=rect

                    elif (row == 2 and col == 0):
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'medium seagreen')

                        view.create_text(75, 255, text='Library', font=("Courier bold", 16), fill='black')
                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoard[(row,col)]=rect

                    elif (row == 2 and col == 2):
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'medium seagreen')

                        view.create_text(380, 255, text='Billiard Room', font=("Courier bold", 16), fill='black')
                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoard[(row,col)]=rect

                    elif (row == 2 and col == 4):
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'medium seagreen')

                        view.create_text(685, 255, text='Dining Room', font=("Courier bold", 16), fill='black')
                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoard[(row,col)]=rect

                    elif (row == 4 and col == 0):
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'medium seagreen')

                        view.create_text(75, 450, text='Conservatory', font=("Courier bold", 16), fill='black')
                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoard[(row,col)]=rect

                    elif (row == 4 and col == 2):
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'medium seagreen')

                        view.create_text(380, 450, text='Ballroom', font=("Courier bold", 16), fill='black')
                        view.itemconfig(rect, tags=(str(rowNumber), str(columnNumber)))
                        gameBoard[(row,col)]=rect

                    elif (row == 4 and col == 4):
                        columnNumber = columnNumber + 1
                        rect = view.create_rectangle(col * gridWidth,
                        row * gridHeight,
                        (col + 1) * gridWidth,
                        (row + 1) * gridHeight,
                        fill = 'medium seagreen')

                        view.create_text(685, 450, text='Kitchen', font=("Courier bold", 16), fill='black')
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

                            view.create_text(685, 545, font=("Courier bold", 16), fill='black')
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
            print("gameBoard")
            print(gameBoard)
            return gameBoard
        
        viewCanvas.pack(side=TOP, fill=BOTH, padx=120, pady=120)
        print(viewCanvas.gettags(CURRENT))
        viewCanvas.itemconfig(CURRENT, fill="LightSalmon3")

        displayCharacters()

        exit_button = Button(root, text="Exit Game", bg="red", fg="white", command=endGame) 
        exit_button.place(x=894, y=134) 

        secret_passageway_study_button = Button(root, text="S", bg="DarkOrchid3", fg="white", command=takeSecretPassageway) 
        secret_passageway_study_button.place(x=252, y=190) 

        secret_passageway_lounge_button = Button(root, text="S", bg="DarkOrchid3", fg="white", command=takeSecretPassageway) 
        secret_passageway_lounge_button.place(x=730, y=190)

        secret_passageway_conservatory_button = Button(root, text="S", bg="DarkOrchid3", fg="white", command=takeSecretPassageway) 
        secret_passageway_conservatory_button.place(x=252, y=522) 

        secret_passageway_kitchen_button = Button(root, text="S", bg="DarkOrchid3", fg="white", command=takeSecretPassageway) 
        secret_passageway_kitchen_button.place(x=730, y=522) 

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