"""
Snake Game

@author: Brendan Bard, Keenan Barber
"""
import pygame

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
GRAY     = ( 127, 127, 127)

SEGMENT_COLOR = GREEN
SEGMENT_SIZE = 10
STEP_SIZE = 10
BACKGROUND_COLOR = WHITE

BORDER_COLOR = BLACK
GAME_SPACE_WIDTH = 400
GAME_SPACE_HEIGHT = 400
GAME_SPACE_PADDING = 20


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
                raise TypeError
        except TypeError:
            print('Coordinates must be in integer format.')

    def __getattr__(self, name):
        '''Validates the name of an attribute the user tries to access.'''
        attr = None
        try:
            if name == 'x':
                attr = self.x
            elif name == 'y':
                attr = self.y
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
        x = 0
        y = 0
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


def in_world(vec):
    print("Checking: " , vec)
    return not (vec.x <= GAME_SPACE_PADDING or vec.x >= GAME_SPACE_PADDING + GAME_SPACE_WIDTH or vec.y <= GAME_SPACE_PADDING or vec.y >= GAME_SPACE_PADDING + GAME_SPACE_HEIGHT)


class SnakeSegment:
    # Constructor
    def __init__(self, x = 0, y = 0):
        self.position = Vector2D(x, y)
        
    def update_position(self, position):
        self.position = position
        
        
    def draw_segment(self, screen):
        pygame.draw.rect(screen, SEGMENT_COLOR, (self.position.x, self.position.y, SEGMENT_SIZE, SEGMENT_SIZE))
        
        
class SnakeBody:
    movementDirection = Vector2D(1, 0)
    
    # Constructor
    def __init__(self, position, initialSegments):
        self.segments = []
        for i in range(initialSegments):
            self.segments.append(SnakeSegment(position.x - (SEGMENT_SIZE * i), position.y))
        
    def update_segments(self):
        i = len(self.segments) - 1
        while i > 0:
            self.segments[i].update_position(self.segments[i-1].position)
            i -= 1
        self.segments[0].update_position(self.segments[0].position + (self.movementDirection * STEP_SIZE))
        

    def draw_segments(self, screen):
        for i in range(len(self.segments)):
            self.segments[i].draw_segment(screen)


def main():
    pygame.init()
    
    width = GAME_SPACE_WIDTH + (2 * GAME_SPACE_PADDING)
    height = GAME_SPACE_HEIGHT + (2 * GAME_SPACE_PADDING)
    screen = pygame.display.set_mode([width,height])
    
    mySnake = SnakeBody(Vector2D(100, 100), 5)
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # -------- Main Program Loop -----------\
    done = False
    while not done:
        # --- Main event loop
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: # If user clicked close
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    mySnake.movementDirection = Vector2D(0, -1)
                elif event.key == pygame.K_DOWN:
                    mySnake.movementDirection = Vector2D(0, 1)
                elif event.key == pygame.K_LEFT:
                    mySnake.movementDirection = Vector2D(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    mySnake.movementDirection = Vector2D(1, 0)
        
            
        # --- Drawing code should go here
        # First, clear the screen
        screen.fill(BORDER_COLOR) 
        pygame.draw.rect(screen, BACKGROUND_COLOR, [GAME_SPACE_PADDING, GAME_SPACE_PADDING, GAME_SPACE_WIDTH, GAME_SPACE_HEIGHT])
        # Now, do your drawing.
        
        mySnake.update_segments()
        mySnake.draw_segments(screen)
        
        font = pygame.font.SysFont('Calibri', 25, True, False) # Gets a font (font, size, bold, italics)
        text = font.render("My text",True,BLACK) # Creates the text (text, anti-aliased, color)
        screen.blit(text, [250, 250]) # Puts image of text on screen (textObj, location)
        # --- Update the screen with what we've drawn.
        pygame.display.update()
    
        # This limits the loop to 60 frames per second (Modified to 2 fps)
        clock.tick(19)
        
    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise e
