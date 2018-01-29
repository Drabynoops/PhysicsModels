
"""
Ultimate Tic-Tac-Toe

@authors: Keenan Barber, Brendan Bard
"""

import inspect
import random

# Point CLASS --------------------------------------
class Point:
    x = 0
    y = 0
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y
        
    def Print(self):
        print("(" + str(self.x) + ", " + str(self.y) + ")")
        
# Point CLASS --------------------------------------
       

# SMALLBOARD CLASS --------------------------------------
class SmallBoard:
    def __init__(self, mark1, mark2):
        self.player1Mark = mark1
        self.player2Mark = mark2
        # 3x3 array
        self.grid = []
        for i in range(3):
            self.grid.append([' ', ' ', ' '])
            
    def ConvertTextRowToGridRow(self, num):
        if num == 0:
            return 0
        elif num == 2:
            return 1
        elif num == 4:
            return 2
        else:
            return 0
            
    def GetRowText(self, row):
        rowStr = ""
        if (row == 0) or (row == 2) or (row == 4):
            gridRow = self.ConvertTextRowToGridRow(row)
            for col in range(3):
                rowStr += " " + self.grid[col][gridRow] + " "
                if col < 2:
                    rowStr += "|"
        
        elif (row == 1) or (row == 3):                
            rowStr += "───+───+───"
        
        return rowStr
    
    def PlaceMark(self, point, mark):
        self.grid[point.x][point.y] = mark
    
    def IsAvailable(self, point):
        return self.grid[point.x][point.y] == ' '

    def Print(self):
        for i in range(5):
            print(self.GetRowText(i))
            
    def IsComplete(self):
        for y in range(3):
            for x in range(3):
                if self.grid[x][y] == ' ':
                    return False
        return True
    
    def CheckForWinner(self):
        return self.player1Mark
        
# SMALLBOARD CLASS --------------------------------------

# LARGEBOARD CLASS --------------------------------------
class LargeBoard:
    def __init__(self, mark1, mark2):
        self.player1Mark = mark1
        self.player2Mark = mark2
        # 3x3 array
        self.grid = []
        for i in range(3):
            self.grid.append([SmallBoard(mark1, mark2), SmallBoard(mark1, mark2), SmallBoard(mark1, mark2)])

            
    def Print(self, targetLargeBoardSquare):
        
        # Prints the 0   1   2 above the board to help with placing marks
        columnIndicator = "  "
        for i in range(targetLargeBoardSquare.x):
            columnIndicator += "              "
        columnIndicator += " " + " 0 " + " " + " 1 " + " " + " 2 " + " "
        print(columnIndicator)
        
        
        for row in range(3): # For each row in large board
            rowIndicator = 0
            for textRow in range(5): # Print 5 text rows
                rowStr = ""
                if (targetLargeBoardSquare.y == row) and (textRow % 2 == 0):
                    rowStr += " " + str(rowIndicator) + " "
                    rowIndicator += 1
                else:
                    rowStr += "   "
                for col in range(3): # Loop through each column
                    if isinstance(self.grid[col][row], SmallBoard):
                        rowStr += self.grid[col][row].GetRowText(textRow)
                    else:
                        if textRow == 2:
                            rowStr += "     " + self.grid[col][row] + "     "
                        else: 
                            rowStr += "           "
                    if col < 2:
                        rowStr += " ║ "
                print(rowStr)
                
            if row < 2:
                print("  " + "═════════════╬═════════════╬═════════════")
        print()
                
    def BoardComplete():
        print("...")
        
# LARGEBOARD CLASS --------------------------------------
        
        
# ULTIMATETICTACTOE CLASS --------------------------------------
class UltimateTicTacToe:
    def __init__(self, mark1, mark2):
        self.player1Mark = mark1
        self.player2Mark = mark2
        self.gameBoard = LargeBoard(mark1, mark2)
        self.nextRequiredLargeBoardSquare = Point(1, 1)
        
        # Pick Starting Player
        self.player1Turn = random.randint(0,1)
        if self.player1Turn == 0:
            self.player1Turn = False
        else:
            self.player1Turn = True
    
    def PrintHeader(self):
        print("*******************************************")
        print("ULTIMATE TIC-TAC-TOE")
        print("*******************************************")
        print("Player 1 -> '" + self.player1Mark + "'             Player 2 -> '" + self.player2Mark + "'")
        print("")
        
    # This function takes in Points as parameters (the large board space, and small board space)
    def PlaceMark(self, gridSpace1, gridSpace2, mark):
        targetSmallBoard = self.gameBoard.grid[gridSpace1.x][gridSpace1.y]
        if isinstance(targetSmallBoard, SmallBoard):
            if targetSmallBoard.IsAvailable(gridSpace2):
                targetSmallBoard.PlaceMark(gridSpace2, mark)
                return True
            else:
                return False
        else:
            return False
        
    def Print(self):
        self.PrintHeader()
        self.gameBoard.Print(self.nextRequiredLargeBoardSquare)
        
    def IsComplete(self):
        return False
    
    def PlayGame(self):
        print("\033[H\033[J") # Clears the output window
        while(self.IsComplete() == False): # While the game is not complete...
            self.Print() # Print Board
            response = self.PromptPlayer()
            if response.lower() == "quit":
                print("Quitting...")
                return
            
            # Convert input to point
            response = self.ConvertStringToPoint(response)
            if self.ValidateCoordinate(response):
                if self.player1Turn:
                    game.PlaceMark(self.nextRequiredLargeBoardSquare, response, self.player1Mark)
                else: 
                    game.PlaceMark(self.nextRequiredLargeBoardSquare, response, self.player2Mark)
                    
                self.nextRequiredLargeBoardSquare = response
                
            else:
                print("The point is INVALID")
                
            self.player1Turn = not self.player1Turn
            print("\033[H\033[J") # Clears the output window
            
    def ConvertStringToPoint(self, inputStr):   
        xNum = -1
        yNum = -1
        
        for char in inputStr:
            if char.isdigit():
                if xNum == -1:
                    xNum = int(char)
                elif yNum == -1:
                    yNum = int(char)
                else:
                    break 
        return Point(xNum, yNum)
        
    def ValidateCoordinate(self, point):
        point.Print()
        if point.x >= 0 and point.x <= 2 and point.y >= 0 and point.y <= 2:
            return True
        else:
            return False
    
    def UserInput(self):
        response = input("   > ")
        return response
        
    def PromptPlayer(self):
        if self.player1Turn:
            print("Player 1's Turn: --------------------------")
        else:
            print("Player 2's Turn: --------------------------")
        print()
        print("Place a mark in the " + self.ConvertPointToEnglish(self.nextRequiredLargeBoardSquare) + " section.")
        print()
        print("Where would you like to place your mark? \nEnter two numbers 0-2. (Example: \"x, y\")", end="")

        return self.UserInput()
    
    def ConvertPointToEnglish(self, point):
        if point.x == 0 and point.y == 0:
            return "upper left"
        elif point.x == 0 and point.y == 1:
            return "left"
        elif point.x == 0 and point.y == 2:
            return "lower left"
        elif point.x == 1 and point.y == 0:
            return "top"
        elif point.x == 1 and point.y == 1:
            return "center"
        elif point.x == 1 and point.y == 2:
            return "bottom"
        elif point.x == 2 and point.y == 0:
            return "upper right"
        elif point.x == 2 and point.y == 1:
            return "right"
        elif point.x == 2 and point.y == 2:
            return "lower right"
        else:
            return "INVALID"
        
# ULTIMATETICTACTOE CLASS --------------------------------------




    





#DisplayBoard()

game = UltimateTicTacToe('X', 'O')

game.PlayGame()


"""

****************************************
ULTIMATE TIC-TAC-TOE
    Authors: Keenan Barber, Brendan Bard
****************************************
Player 1 -> 'X'          Player 2 -> 'O'

                0   1   2
    |   |    ║    |   |    ║    |   |    
 ───+───+─── ║ ───+───+─── ║ ───+───+─── 
    |   |    ║    |   |    ║    |   |    
 ───+───+─── ║ ───+───+─── ║ ───+───+─── 
    |   |    ║    |   |    ║    |   |    
═════════════╬═════════════╬═════════════
    |   |    ║    |   |    ║    |   |    
 ───+───+─── ║ ───+───+─── ║ ───+───+─── 
    |   |    ║    |   |    ║    |   |    
 ───+───+─── ║ ───+───+─── ║ ───+───+─── 
    |   |    ║    |   |    ║    |   |    
═════════════╬═════════════╬═════════════
    |   |    ║    |   |    ║    |   |    
 ───+───+─── ║ ───+───+─── ║ ───+───+─── 
    |   |    ║    |   |    ║    |   |    
 ───+───+─── ║ ───+───+─── ║ ───+───+─── 
    |   |    ║    |   |    ║    |   |    

Player 1's Turn: -----------------------

Where would you like to place your 
mark? (Format: "x, y")
    > (0, 2)








════════════╬═════════════╬═════════════
            ║    |   |    ║    |   |    
            ║ ───+───+─── ║ ───+───+─── 
     X      ║    |   |    ║    |   |    
            ║ ───+───+─── ║ ───+───+─── 
            ║    |   |    ║    |   |    




first text row
    rowStr = ""
    
    if(grid[0])
   
"""




























