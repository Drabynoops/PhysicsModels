
import pygame
from color import Color
import random
import math
from vec2d import Vec2d

ASTEROID_VERTEX_COUNT_MIN = 7
ASTEROID_VERTEX_COUNT_MAX = 14
ASTEROID_RADIUS_NOISE = 4

class Asteroid(pygame.sprite.Sprite):
    # Constructor
    def __init__(self, pos, vel, radius):
        super(Asteroid, self).__init__()
        
        # Visual variables
        self.line_thickness = 2
        self.line_color = Color.WHITE
        self.fill_color = Color.BLACK
        
        # Physics variables
        self.pos = pos
        self.vel = vel
        self.mass = radius * radius # Using the asteroid's radius to determine the mass
        self.mom = self.vel * self.mass
        self.force = Vec2d(0,0)
        
        # Give initial spin
        self.angular_velocity = 0
        if random.randint(0, 1) == 0:
            self.angular_velocity = random.random() * 1
        else:
            self.angular_velocity = random.random() * -1
        
        # Asteroid details
        self.rotation_angle = 0
        self.vertices = [] # A list of points --> EXAMPLE: [(50, 50), (70, 50), (70, 70)]
        
        # Variables for collision and the sprite
        self.radius = radius
        self.image = pygame.Surface([self.radius * 2, self.radius * 2])
        self.rect = self.image.get_rect()
        
        # Generate the vertices for the asteroid
        angleStep = 360 / random.randint(ASTEROID_VERTEX_COUNT_MIN, ASTEROID_VERTEX_COUNT_MAX)
        currentStep = 0
        while currentStep <= (360 - angleStep):
            rad = currentStep * (math.pi / 180)
            noise = random.randint(int(-1 * ASTEROID_RADIUS_NOISE), int(ASTEROID_RADIUS_NOISE)) # Adds noise to the shape
            newVertex = [
                ((self.radius + noise) * math.cos(rad)), 
                ((self.radius + noise) * math.sin(rad))
            ]

            self.vertices.append(newVertex)
            currentStep += angleStep
            
    # Sets the color and line thickness of asteroid
    def set_visual_details(self, line_color, line_thickness, fill_color):
        self.line_color = line_color
        self.line_thickness = line_thickness
        self.fill_color = fill_color
    
    def collide_with_asteroid(self, other):
        # Calculate the angular velocity
        r = ((other.pos - self.pos).normalized() * self.radius) - self.pos
        v = other.vel
        self.angular_velocity = ((r.x * v.y) - (r.y * v.x)) / ((r.x * r.x) + (r.y * r.y))
        
        # Calculate the velocity vectors for each asteroid
        d = math.sqrt(math.pow(self.pos.x - other.pos.x, 2) + math.pow(self.pos.y - other.pos.y, 2))
        n = (other.pos - self.pos) / d
        p = 2 * ((self.vel.dot(n)) - (other.vel.dot(n))) / (self.mass + other.mass)
        final_vel_1 = self.vel - (p * other.mass) * n
        final_vel_2 = other.vel + (p * self.mass) * n
        
        # Calculate final momentum for both asteroids
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
        
        # SCIENCE!
        self.mom += self.force*dt
        self.vel.copy_in(self.mom/self.mass)
        self.pos += self.vel*dt
        
        # Faking the angular velocity / rotation a bit...
        self.rotation_angle += (self.angular_velocity)
        
        # Update collider's position
        self.rect.x = self.pos.x - self.radius
        self.rect.y = self.pos.y - self.radius

    def draw(self, screen):        
        #self.update_vertices()
        updatedVertices = []
        for point in self.vertices:
            updatedVertex = self.rotate_point_around_pivot(Vec2d(point[0], point[1]) + self.pos, self.pos, self.rotation_angle)
            updatedVertices.append(updatedVertex)
        
        pygame.draw.polygon(screen, self.fill_color, updatedVertices, 0)
        pygame.draw.lines(screen, self.line_color, True, updatedVertices, self.line_thickness)
        
        # To visualize the collider
        #pygame.draw.circle(screen, (0, 255, 0), [self.rect.x + self.radius, self.rect.y + self.radius], self.radius)
        
