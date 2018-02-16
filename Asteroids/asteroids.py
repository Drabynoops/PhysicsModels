import pygame
from pygame import init, quit
import math
import random

from color import Color
from coords import Coords
from vec2d import Vec2d

ASTEROID_MIN_RADIUS = 20
ASTEROID_MAX_RADIUS = 30
ASTEROID_VERTEX_COUNT_MIN = 7
ASTEROID_VERTEX_COUNT_MAX = 14
ASTEROID_RADIUS_NOISE = 10

BACKGROUND_COLOR = BLACK
LINE_COLOR = WHITE
LINE_THICKNESS = 2


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
        self.draw_screen.fill(Color.WHITE)
        self.screen_center = Vec2d(width/2, height/2)
        self.coords = Coords(self.screen_center.copy(), 1, True)

def main():
    input()

    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise 
