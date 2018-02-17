
import pygame
import random
import math
from vec2d import Vec2d

ASTEROID_MIN_RADIUS = 20
ASTEROID_MAX_RADIUS = 30
ASTEROID_VERTEX_COUNT_MIN = 7
ASTEROID_VERTEX_COUNT_MAX = 14
ASTEROID_RADIUS_NOISE = 6

LINE_COLOR = (255, 255, 255)
LINE_THICKNESS = 2


class Asteroid(pygame.sprite.Sprite):
    # Constructor
    def __init__(self, pos, vel, mass):
        super(Asteroid, self).__init__()
        
        # Physics variables
        self.pos = pos
        self.vel = vel
        self.mass = mass
        self.mom = self.vel * self.mass
        self.force = Vec2d(0,0)
        
        # Asteroid details
        self.rotationAngle = 0
        self.vertices = []#[(50, 50), (70, 50), (70, 70)]
        self.asteroidRadius = random.randint(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS) 
        
        # Variables for collision and the sprite
        self.radius = self.asteroidRadius
        self.image = pygame.Surface(2*[self.asteroidRadius*2])
        self.rect = self.image.get_rect()
        
        # Generate the vertices for the asteroid
        angleStep = 360 / random.randint(ASTEROID_VERTEX_COUNT_MIN, ASTEROID_VERTEX_COUNT_MAX)
        currentStep = 0
        while currentStep <= (360 - angleStep):
            rad = currentStep * (math.pi / 180)
            noise = random.randint(int(-1 * ASTEROID_RADIUS_NOISE), 0) # Adds noise to the shape
            newVertex = [
                ((self.asteroidRadius + noise) * math.cos(rad)), 
                ((self.asteroidRadius + noise) * math.sin(rad))
            ]

            self.vertices.append(newVertex)
            currentStep += angleStep
    
    def collide_with_asteroid(self, other):
        d = math.sqrt(math.pow(self.pos.x - other.pos.x, 2) + math.pow(self.pos.y - other.pos.y, 2))
        n = (other.pos - self.pos) / d
        p = 2 * ((self.vel.dot(n)) - (other.vel.dot(n))) / (self.mass + other.mass)
        final_vel_1 = self.vel - (p * self.mass) * n
        final_vel_2 = other.vel + (p * other.mass) * n
        
        # Calculate final velocities for both asteroids
        self.mom = self.mass * final_vel_1
        other.mom = other.mass * final_vel_2
    
    def rotate_point_around_pivot(self, point, pivot, angle):
        newPoint = point.copy()
        rad = angle * (math.pi / 180)
        s = math.sin(rad);
        c = math.cos(rad);

        # translate point back to origin:
        newPoint.x -= pivot.x;
        newPoint.y -= pivot.y;
        
        # rotate point
        xnew = newPoint.x * c - newPoint.y * s;
        ynew = newPoint.x * s + newPoint.y * c;
        
        # translate point back:
        newPoint.x = xnew + pivot.x;
        newPoint.y = ynew + pivot.y;
        return newPoint;

    def update(self, dt):
        super(Asteroid, self).update()
        
        self.mom += self.force*dt
        self.vel.copy_in(self.mom/self.mass)
        self.pos += self.vel*dt
        self.rotationAngle += 1
        
        # Update colliders position
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def draw(self, screen):        
        #self.update_vertices()
        updatedVertices = []
        for point in self.vertices:
            updatedVertex = self.rotate_point_around_pivot(Vec2d(point[0], point[1]) + self.pos, self.pos, self.rotationAngle)
            updatedVertices.append(updatedVertex)
        pygame.draw.lines(screen, LINE_COLOR, True, updatedVertices, LINE_THICKNESS)
        
        # To visualize the collider
        #.draw.circle(screen, (0, 255, 0), self.pos.int(), self.asteroidRadius)

