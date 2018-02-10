"""
Snake Game

@author: Brendan Bard, Keenan Barber
"""
import pygame
import random

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
GRAY     = ( 127, 127, 127)

SEGMENT_COLOR = BLACK
FOOD_COLOR = BLACK
CELL_SIZE = 10
BACKGROUND_COLOR = GRAY
BORDER_COLOR = BLACK

class Vector2D:
    '''Creates a 2D point that can work with mathimatical operations.'''

    def __init__(self, x, y):
        '''Initialize the x and y coordinates.'''
        self.x = x
        self.y = y
    
    def __repr__(self):
        '''Create the output for it Vector2D is put into print().'''
        return '(' + str(self.x) + ',' + str(self.y) + ')'

    def __setattr__(self, name, value):
        '''Validate user input for x and y coordinates.'''
        try:
            if isinstance(value, int):
                if name == 'x' or name == 'y':
                    super(Vector2D, self).__setattr__(name, value)
                else:
                    raise AttributeError
            else:
                raise TypeError
        except TypeError:
            print('Coordinate {} must be in integer format.'.format(name))
        except AttributeError:
            print('No attribute named {}.'.format(name))

    def __getattr__(self, name):
        '''Validates the name of an attribute the user tries to access.'''
        attr = None
        try:
            if name == 'x' or name == 'y':
                attr = super(Vector2D, self).__getattr__(name)
            else:
                raise AttributeError
        except AttributeError:
            print('No attribute {}. Valid attributes are x and y.'.format(name))
        return attr

    def __eq__(self, other):
        '''Confirm that other is a point and then return if they are equal.'''
        equal = False
        try:
            if isinstance(other, Vector2D):
                if self.x == other.x and self.y == other.y:
                    equal = True
            else:
                raise TypeError
        except TypeError:
            print('Can not compare Vector2D and {} for equality.'.format(type(other)))
        
        
        return equal

    def __add__(self, other):
        '''Confirm that other is a point and then create their sums.'''
        try:
            if isinstance(other, Vector2D):
                x = self.x + other.x
                y = self.y + other.y
            else:
                raise TypeError
        except:
            print('Cannot add {} to Vector2D. Must be another Vector2D'.format(type(other)))
        return Vector2D(x, y)

    __radd__ = __add__

    def __sub__(self, other):
        '''Confirm that other is a point.
    
        Then subtract with other on the right side.
        '''
        try:
            if isinstance(other, Vector2D):
                x = self.x - other.x
                y = self.y - other.y
            else:
                raise TypeError
        except:
            print('Cannot add {} to Vector2D. Must be another Vector2D'.format(type(other)))
        return Vector2D(x, y)

    def __rsub__(self, other):
        '''Confirm that other is a point.
        
        Then subtract with other on the left side.
        '''
        try:
            if isinstance(other, Vector2D):
                x = other.x - self.x
                y = other.y - self.y
            else:
                raise TypeError
        except:
            print('Cannot add {} to Vector2D. Must be another Vector2D'.format(type(other)))
        return Vector2D(x, y)
    
    def __mul__(self, other):
        '''Confirm that other is an integer and perform scalar multiplication.'''
        try:
            if isinstance(other, int):
                x = other * self.x
                y = other * self.y
            else:
                raise TypeError
        except:
            print('Can not multiple by {}. Must be int.'.format(type(other)))
        return Vector2D(x, y)

    __rmul__ = __mul__


class Food:
    # Constructor
    def __init__(self, vec):
        self.position = vec
        
    def move(self, vec):
        self.position = vec
        
    def draw(self, screen):
        pygame.draw.rect(screen, FOOD_COLOR, (self.position.x, self.position.y, CELL_SIZE, CELL_SIZE))
        

class SnakeSegment:
    # Constructor
    def __init__(self, x = 0, y = 0):
        self.position = Vector2D(x, y)
        
    def update_position(self, position):
        self.position = position
        
        
    def draw(self, screen):
        pygame.draw.rect(screen, SEGMENT_COLOR, (self.position.x, self.position.y, CELL_SIZE, CELL_SIZE))
        
        
class SnakeBody:
    movementDirection = Vector2D(1, 0)
    
    # Constructor
    def __init__(self, position, initialSegments):
        self.segments = []
        for i in range(initialSegments):
            self.segments.append(SnakeSegment(position.x - (CELL_SIZE * i), position.y))
        
    def update_segments(self):
        i = len(self.segments) - 1
        while i > 0:
            self.segments[i].update_position(self.segments[i-1].position)
            i -= 1
        self.segments[0].update_position(self.segments[0].position + (self.movementDirection * CELL_SIZE))


    def draw(self, screen):
        for i in range(len(self.segments)):
            self.segments[i].draw(screen)
        

class SnakeGame:

    def __init__(self, width, height):
        pygame.init()

        self.borderThickness = 5
        self.padding = 20
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode([width, height])
        self.mySnake = SnakeBody(Vector2D(50, 50), 5)
        self.food = Food(self.get_random_position())
        self.state = self.play
        self.done = False

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

    def execute_game_loop(self):
        # -------- Main Program Loop -----------\
        while not self.done:
            self.state()
            
        pygame.quit()

    def play(self):
        # --- Main event loop
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: # If user clicked close
                    self.done = True
                elif event.type == pygame.KEYDOWN:
                    # Move Snake
                    if event.key == pygame.K_UP:
                        self.mySnake.movementDirection = Vector2D(0, -1)
                    elif event.key == pygame.K_DOWN:
                        self.mySnake.movementDirection = Vector2D(0, 1)
                    elif event.key == pygame.K_LEFT:
                        self.mySnake.movementDirection = Vector2D(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.mySnake.movementDirection = Vector2D(1, 0)
            
            
                
                
            # --- Drawing code should go here
            # First, clear the screen
            self.screen.fill(BACKGROUND_COLOR) 
            pygame.draw.rect(self.screen, BORDER_COLOR, (self.padding - self.borderThickness, self.padding - self.borderThickness, self.width - (2 * self.padding) + (2 * self.borderThickness), self.height - (2 * self.padding) + (2 * self.borderThickness)))
            pygame.draw.rect(self.screen, BACKGROUND_COLOR, (self.padding, self.padding, self.width - (2 * self.padding), self.height - (2 * self.padding)))
            # Now, do your drawing.
            
            self.mySnake.update_segments()
            self.wrap_snake()
            self.mySnake.draw(self.screen)
            
            self.food.draw(self.screen)
            
            font = pygame.font.SysFont('Calibri', 25, True, False) # Gets a font (font, size, bold, italics)
            text = font.render("My text",True,BLACK) # Creates the text (text, anti-aliased, color)
            self.screen.blit(text, [250, 250]) # Puts image of text on screen (textObj, location)
            # --- Update the screen with what we've drawn.
            pygame.display.update()
        
            # This limits the loop to 60 frames per second (Modified to 12 fps)
            self.clock.tick(4)
            
    def get_random_position(self):
        newX = random.randint(self.padding, self.width - (2 * self.padding))
        newY = random.randint(self.padding, self.height - (2 * self.padding))
        return self.snap_to_grid(Vector2D(newX, newY))
    
    def snap_to_grid(self, vec):
        newX = int(round(vec.x / CELL_SIZE)) * CELL_SIZE
        newY = int(round(vec.y / CELL_SIZE)) * CELL_SIZE
        return Vector2D(newX, newY)
    
    def wrap_snake(self):
        # Wrap snake around x direction
        if(self.mySnake.segments[0].position.x < self.padding):
            self.mySnake.segments[0].position.x = self.width - self.padding - CELL_SIZE
        if(self.mySnake.segments[0].position.x > self.width - self.padding - CELL_SIZE):
            self.mySnake.segments[0].position.x = self.padding
        # Wrap snake around y direction
        if(self.mySnake.segments[0].position.y < self.padding):
            self.mySnake.segments[0].position.y = self.height - self.padding - CELL_SIZE
        if(self.mySnake.segments[0].position.y > self.height - self.padding - CELL_SIZE):
            self.mySnake.segments[0].position.y = self.padding
            

def main():
        
    game = SnakeGame(300, 400)

    game.execute_game_loop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise e