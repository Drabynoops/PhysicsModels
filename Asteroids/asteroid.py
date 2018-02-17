from pygame import draw
from color import Color

import random
import math

class Asteroid:
    ASTEROID_MIN_RADIUS = 20
    ASTEROID_MAX_RADIUS = 30
    ASTEROID_VERTEX_COUNT_MIN = 7
    ASTEROID_VERTEX_COUNT_MAX = 14
    ASTEROID_RADIUS_NOISE = 10

    BACKGROUND_COLOR = Color.BLACK
    LINE_COLOR = Color.WHITE
    LINE_THICKNESS = 2

    # Constructor
    def __init__(self, x=0, y=0):
        self.position = Vec2d(x, y)
        self.vertices = []  # [(50, 50), (70, 50), (70, 70)]

        self.asteroidRadius = random.randint(
            Asteroid.ASTEROID_MIN_RADIUS, Asteroid.ASTEROID_MAX_RADIUS)

        # Generate the vertices for the asteroid
        angleStep = 360 / \
            random.randint(Asteroid.ASTEROID_VERTEX_COUNT_MIN,
                           Asteroid.ASTEROID_VERTEX_COUNT_MAX)
        currentStep = 0
        while currentStep <= (360 - angleStep):
            rad = currentStep * (math.pi / 180)
            # Adds noise to the shape
            noise = random.randint(-1 * Asteroid.ASTEROID_RADIUS_NOISE,
                                   Asteroid.ASTEROID_RADIUS_NOISE)
            newVertex = [
                ((self.asteroidRadius + noise) * math.cos(rad)) + self.position.x,
                ((self.asteroidRadius + noise) * math.sin(rad)) + self.position.y
            ]

            self.vertices.append(newVertex)
            currentStep += angleStep

    def draw(self, screen):
        pygame.draw.lines(screen, Asteroid.LINE_COLOR, True,
                          self.vertices, Asteroid.LINE_THICKNESS)
