
"""
Ultimate Tic-Tac-Toe

@authors: Keenan Barber, Brendan Bard
"""

from enum import Enum
import random


# ACTIONTYPE ENUM --------------------------------------
class ActionType(Enum):
    '''Define the type of actions that the program allows the player to take.'''
    ANYWHERE = 1
    TARGET = 2
# ACTIONTYPE ENUM --------------------------------------


# PLAYERSTATE ENUM --------------------------------------
class PlayerState(Enum):
    '''Define which player's turn it is.'''
    PLAYER1 = 1
    PLAYER2 = 2
# PLAYERSTATE ENUM --------------------------------------

# POINT CLASS --------------------------------------
class Point:
    '''Define the a point in the coordinate plane(grid).'''
    x = 0
    y = 0
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y
        
    def print(self):
        print("(" + str(self.x) + ", " + str(self.y) + ")")
# POINT CLASS --------------------------------------
        

# END GAME CLASS ---------------------------------
class GridCompletion:
    '''Test a supplied 3x3 grid/board against all possible win cons.'''
    def __init__(self):
        self.win_cons = [
            [Point(0, 0), Point(1, 0), Point(2, 0)],
            [Point(0, 1), Point(1, 1), Point(2, 1)],
            [Point(0, 2), Point(1, 2), Point(2, 2)],

            [Point(0, 0), Point(0, 1), Point(0, 2)],
            [Point(1, 0), Point(1, 1), Point(1, 2)],
            [Point(2, 0), Point(2, 1), Point(2, 2)],

            [Point(0, 0), Point(1, 1), Point(2, 2)],
            [Point(0, 2), Point(1, 1), Point(2, 0)]
        ]

    def has_winner(self, board):
        '''Test the provided board.'''
        for row in self.win_cons:
            point_one = board.grid[row[0].x][row[0].y]
            point_two = board.grid[row[1].x][row[1].y]
            if point_one == point_two and point_one != ' ' and isinstance(point_one, str):
                point_three = board.grid[row[2].x][row[2].y]
                if point_one == point_three:
                    return True
        return False


# SMALLBOARD CLASS --------------------------------------
class SmallBoard:
    '''Define a 3x3 grid that exists inside another 3x3 grid.'''
    def __init__(self, mark1, mark2):
        self.player_one_mark = mark1
        self.player_two_mark = mark2
        # 3x3 array
        self.grid = []
        for i in range(3):
            self.grid.append([' ', ' ', ' '])
            
    def convert_text_row_to_grid_row(self, num):
        '''Provide the row in the grid to be printed relative to the text row.'''
        if num == 0:
            return 0
        elif num == 2:
            return 1
        elif num == 4:
            return 2
        else:
            return 0

    def get_row_text(self, row):
        '''Return the row of text to be printed determined the provided row.'''
        row_str = ""
        if (row == 0) or (row == 2) or (row == 4):
            grid_row = self.convert_text_row_to_grid_row(row)
            for col in range(3):
                row_str += " " + self.grid[col][grid_row] + " "
                if col < 2:
                    row_str += "|"
        elif (row == 1) or (row == 3):
            row_str += "───┼───┼───"

        return row_str

    def place_mark(self, point, mark):
        '''Assign a value to a point in the grid.'''
        self.grid[point.x][point.y] = mark

    def is_available(self, point):
        '''Returns whether or not a point has been taken.'''
        return self.grid[point.x][point.y] == ' '

    def print(self):
        '''Print the grid.'''
        for i in range(5):
            print(self.get_row_text(i))

    def is_complete(self):
        '''Determines if the grid is filled.'''
        for y in range(3):
            for x in range(3):
                if self.grid[x][y] == ' ':
                    return False
        return True
# SMALLBOARD CLASS --------------------------------------


# LARGEBOARD CLASS --------------------------------------
class LargeBoard:
    '''Creates and runs the large play board for ultimate tic-tac-toe.'''
    def __init__(self, mark1, mark2):
        self.player_one_mark = mark1
        self.player_two_mark = mark2
        # 3x3 array
        self.grid = []
        for i in range(3):
            self.grid.append([SmallBoard(mark1, mark2),
                              SmallBoard(mark1, mark2),
                              SmallBoard(mark1, mark2)])


    def print(self, target_large_board_square, action_type):
        '''Print out the grid for the big board.
            Include the smaller boards, which get called when they
            need to be printed.
        '''
        if action_type == ActionType.TARGET:
            # Prints the 0   1   2 above the board to help with placing marks
            column_indicator = "  "
            for i in range(target_large_board_square.x):
                column_indicator += "              "
            column_indicator += " " + " 0 " + " " + " 1 " + " " + " 2 " + " "
            print(column_indicator)
        if action_type == ActionType.ANYWHERE:
            print("    0   1   2     3   4   5     6   7   8")

        row_indicator = 0
        for row in range(3): # For each row in large board
            for text_row in range(5): # Print 5 text rows
                row_str = ""
                if action_type == ActionType.TARGET:
                    if (target_large_board_square.y == row) and (text_row % 2 == 0):
                        row_str += " " + str(row_indicator) + " "
                        row_indicator += 1
                    else:
                        row_str += "   "
                if action_type == ActionType.ANYWHERE:
                    if text_row % 2 == 0:
                        row_str += " " + str(row_indicator) + " "
                        row_indicator += 1
                    else:
                        row_str += "   "

                for col in range(3): # Loop through each column
                    if isinstance(self.grid[col][row], SmallBoard):
                        row_str += self.grid[col][row].get_row_text(text_row)
                    else:
                        if text_row == 2:
                            row_str += "     " + self.grid[col][row] + "     "
                        else:
                            row_str += "           "
                    if col < 2:
                        row_str += " ║ "
                print(row_str)

            if row < 2:
                print("  " + "═════════════╬═════════════╬═════════════")
        print()

    def complete_small_board(self, target_large_board_square, mark):
        '''Replace a small board with a marker when a player completes it.'''
        self.grid[target_large_board_square.x][target_large_board_square.y] = mark
# LARGEBOARD CLASS --------------------------------------


# ULTIMATETICTACTOE CLASS --------------------------------------
class UltimateTicTacToe:
    '''Defines and executes a game of Ultimate Tic Tac Toe!'''
    def __init__(self, mark1, mark2):
        self.player_one_mark = mark1
        self.player_two_mark = mark2
        self.game_board = LargeBoard(mark1, mark2)
        self.next_required_large_board_square = Point(1, 1)
        self.is_complete = False
        self.grid_completion = GridCompletion()
        self.action_type = ActionType.ANYWHERE

        # Pick Starting Player (using PlayerState enum)
        self.player_turn = PlayerState(random.randint(1, 2))
    
    def print_header(self):
        '''Prints the headers for the tic-tac-toe game.'''
        print("*******************************************")
        print("           ULTIMATE TIC-TAC-TOE            ")
        print("*******************************************")
        print("Player 1 -> '" + self.player_one_mark +
              "'             Player 2 -> '" + self.player_two_mark + "'")
        print("")

    # This function takes in Points as parameters (the large board space, and small board space)
    def place_mark(self, grid_space_one, grid_space_two, mark):
        '''Takes the user input to place the mark in the designated locations.'''
        target_small_board = self.game_board.grid[grid_space_one.x][grid_space_one.y]
        if isinstance(target_small_board, SmallBoard):
            if target_small_board.is_available(grid_space_two):
                target_small_board.place_mark(grid_space_two, mark)
                return target_small_board
            else:
                return False
        else:
            return False

    def print(self):
        '''Prints an updated instance of the ui and large board.'''
        self.print_header()
        self.game_board.print(self.next_required_large_board_square, self.action_type)

    def play_game(self):
        '''Executes the main loop of the game.'''
        self.clear_screen()
        while self.is_complete is False: # While the game is not complete...
            self.clear_screen()
            self.print() # Print Board

            if self.player_turn == PlayerState.PLAYER1:
                turn_player_mark = self.player_one_mark
            else:
                turn_player_mark = self.player_two_mark

            # Commands!
            response = self.prompt_player()
            if response.lower() == "quit":
                print("Quitting...")
                return

            # Convert input to point
            response = self.convert_string_to_point(response)
            if self.validate_coordinate(response):
                if self.action_type == ActionType.ANYWHERE:
                    self.next_required_large_board_square.x = response.x // 3
                    self.next_required_large_board_square.y = response.y // 3
                    response.x = response.x % 3
                    response.y = response.y % 3
                target_small_board = game.place_mark(self.next_required_large_board_square,
                                                     response, turn_player_mark)
                if target_small_board:
                    # Switch player state
                    if self.player_turn == PlayerState.PLAYER1:
                        self.player_turn = PlayerState.PLAYER2
                    else:
                        self.player_turn = PlayerState.PLAYER1

                    if self.grid_completion.has_winner(target_small_board):
                        self.game_board.complete_small_board(self.next_required_large_board_square,
                                                             turn_player_mark)
                        if self.grid_completion.has_winner(self.game_board):
                            self.is_complete = True
                    self.next_required_large_board_square = response
                    if isinstance(self.game_board.grid[response.x][response.y], str):
                        self.action_type = ActionType.ANYWHERE
                    else:
                        self.action_type = ActionType.TARGET
                else:
                    print("That point is already taken!")
                    input("Press enter to continue...") # Wait for player to realize
            else:
                print("The point is INVALID.")
                input("Press enter to continue...")
                
        self.clear_screen()
        print("The game ends with ", turn_player_mark, " as winner!!!")
        print("The final board!!!")
        self.game_board.print(self.next_required_large_board_square, ActionType.ANYWHERE)

    def convert_string_to_point(self, input_str):
        '''Convert an input string to a numberical point.'''
        x_num = -1
        y_num = -1

        for char in input_str:
            if char.isdigit():
                if x_num == -1:
                    x_num = int(char)
                elif y_num == -1:
                    y_num = int(char)
                else:
                    break
        return Point(x_num, y_num)

    def validate_coordinate(self, point):
        '''Confirm that the user is selecting a point that exists.'''
        max_range = 3 if self.action_type == ActionType.TARGET else 9
        if point.x in range(max_range) and point.y in range(max_range):
            return True
        else:
            return False

    def user_input(self):
        '''Capture the user input.'''
        response = input("   > ")
        return response
        
    def prompt_player(self):
        '''Prompt the user for their next move.'''
        if self.player_turn == PlayerState.PLAYER1:
            print("Player 1's Turn: --------------------------")
        else:
            print("Player 2's Turn: --------------------------")
        print()
        if self.action_type == ActionType.TARGET:
            print("Place a mark in the " +
                  self.convert_point_to_english(self.next_required_large_board_square) +
                  " section.")
            print()
            print("Where would you like to place your mark?")
            print("Enter two numbers 0-2. (Example: \"x, y\")", end="")
        if self.action_type == ActionType.ANYWHERE:
            print("Place a mark in any spot that has not been taken.")
            print()
            print("Where would you like to place your mark?")
            print("Enter two numbers 0-9. (Example: \"x, y\")", end="")
        return self.user_input()

    def convert_point_to_english(self, point):
        '''Convert the necessary grid location to be displayed.'''
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

    def clear_screen(self):
        '''Print a bunch of stuff to clear the screen.'''
        print("\033[H\033[J")
# ULTIMATETICTACTOE CLASS --------------------------------------




    





#DisplayBoard()

game = UltimateTicTacToe('X', 'O')

game.play_game()


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
    row_str = ""
    
    if(grid[0])
   
"""




























