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
    x = 0
    y = 0
    
    # Constructor
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        
    # Operator Overload
    def __add__(self, b):
        return Vector2D(self.x + b.x, self.y + b.y)
    
    # Operator Overload (Example: vec * 6)
    def __mul__(self, b):
        return Vector2D(self.x * b, self.y * b)
    
    # tostring
    def __repr__(self):
        return ("<" + str(self.x) + ", " + str(self.y) + ">")


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
    
    width = 800
    height = 600
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
        screen.fill(BACKGROUND_COLOR) 
        # Now, do your drawing.
        
        mySnake.update_segments()
        mySnake.draw_segments(screen)
        
        font = pygame.font.SysFont('Calibri', 25, True, False) # Gets a font (font, size, bold, italics)
        text = font.render("My text",True,BLACK) # Creates the text (text, anti-aliased, color)
        screen.blit(text, [250, 250]) # Puts image of text on screen (textObj, location)
        # --- Update the screen with what we've drawn.
        pygame.display.update()
    
        # This limits the loop to 60 frames per second (Modified to 2 fps)
        clock.tick(2)
        
    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise e
