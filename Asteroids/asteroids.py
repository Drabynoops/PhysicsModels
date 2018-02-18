import pygame
from pygame import init, quit
import math
import random
from enum import Enum

from coords import Coords
from vec2d import Vec2d


BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
GRAY     = ( 127, 127, 127)

ASTEROID_MIN_RADIUS = 20
ASTEROID_MAX_RADIUS = 30
ASTEROID_VERTEX_COUNT_MIN = 7
ASTEROID_VERTEX_COUNT_MAX = 14
ASTEROID_RADIUS_NOISE = 10

BACKGROUND_COLOR = BLACK
LINE_COLOR = WHITE
LINE_THICKNESS = 2


class Player(pygame.sprite.Sprite):

    def __init__(self, radius):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        
        # Assign a width an height because of the
        self.x = 0
        self.y = 0 
        self.radius = radius
        self.__width = self.radius + self.radius
        self.__height = self.radius + self.radius
        self.__line_thickness = 1
        self.__local_position = [self.__width // 2, self.__height // 2]

        # Create an image of the block, and fill it with a color
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([self.__width, self.__height])
        pygame.draw.circle(self.image, WHITE, self.__position, self.radius, self.__line_thickness)

    def draw(self, target):
        target.blit(self.image, (0, 0))

class Asteroid:
    # Constructor
    def __init__(self, x = 0, y = 0):
        self.position = Vec2d(x, y)
        self.vertices = []#[(50, 50), (70, 50), (70, 70)]

        self.asteroidRadius = random.randint(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS) 
        
        # Generate the vertices for the asteroid
        angleStep = 360 / random.randint(ASTEROID_VERTEX_COUNT_MIN, ASTEROID_VERTEX_COUNT_MAX)
        currentStep = 0
        while currentStep <= (360 - angleStep):
            rad = currentStep * (math.pi / 180)
            noise = random.randint(-1 * ASTEROID_RADIUS_NOISE, ASTEROID_RADIUS_NOISE) # Adds noise to the shape
            newVertex = [
                ((self.asteroidRadius + noise) * math.cos(rad)) + self.position.x, 
                ((self.asteroidRadius + noise) * math.sin(rad)) + self.position.y
            ]

            self.vertices.append(newVertex)
            currentStep += angleStep

    def draw(self, screen):
        pygame.draw.lines(screen, LINE_COLOR, True, self.vertices, LINE_THICKNESS)
        

class Game:

    def __init__(self, width, height):
        pygame.init()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode([width,height])
        self.draw_screen = self.screen.copy()
        self.draw_screen.fill(BLACK)
        self.screen_center = Vec2d(width/2, height/2)
        self.coords = Coords(self.screen_center.copy(), 1, True)
        self.player = Player(50)

        self.state = self.play # The game state
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
            
        # --- Drawing code should go here
        # First, clear the screen
        self.screen.fill(( 255, 255, 255)) 
        
        # Now, do your drawing.
        self.player.draw(self.screen)
        
        # --- Update the screen with what we've drawn.
        pygame.display.update()
    
        # This limits the loop to 60 frames per second (Modified to 12 fps)
        self.clock.tick(60)

    def run(self):
        pass

def main():
    game = Game(400, 300)
    game.execute_game_loop()

    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise 
