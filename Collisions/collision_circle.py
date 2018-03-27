import pygame

from color import Color
from vec2d import Vec2d

class CollisionCircle:

    def __init__(self, radius, position, velocity):
        self.radius = radius
        self.mass = 1.522 * self.radius
        self.position = position
        self.velocity = velocity
        
        self.momentum = self.mass * self.velocity
        self.color = Color.BLUE

    def collide_with_circle(self, other):
        restitution_coefficient = 1
        distance = (self.position - other.position).mag()

        v1 = self.velocity
        v2 = other.velocity

        m1 = self.mass
        m2 = other.mass

        r1 = self.radius
        r2 = other.radius

        if distance <= r1 + r2: # Collision
            overlap = r1 + r2 - distance
            self.move_position(overlap / 2)
            other.move_position(-overlap / 2)

            reduced_mass = (m1 * m2) / (m1 + m2)
            collision_normal = (self.position - other.position).hat()
            # TODO: Get this collision calculation working correctly
            impulse = -(1 + restitution_coefficient) * reduced_mass * (v1 - v2) * collision_normal #* collision_normal
            self.set_momentum(self.momentum + impulse)
            self.set_momentum(self.momentum - impulse)


            self.set_velocity(self.momentum / self.mass)
            other.set_velocity(other.momentum / other.mass)

    def collide_with_wall(self, other):
        restitution_coefficient = 1
        collision_normal = other.position.perpendicular_normal()
        distance = collision_normal * (self.position.mag() - other.position.mag())

        v1 = self.velocity
        # No v2 as it isn't moving

        m1 = self.mass
        # No m2 as it is infinite

        r1 = self.radius
        # No r2 as it has no radius

        if distance.mag() < r1: # Collision
            overlap = r1 - distance
            self.move_position(overlap)

            reduced_mass = m1 # Since m2 would be infinite is reduces to m1
            
            impulse = -(1 + restitution_coefficient) * reduced_mass * v1 * collision_normal#**2

            self.set_momentum(self.momentum + impulse)
            self.set_velocity(self.momentum / self.mass)

    def set_position(self, new_pos):
        self.position = new_pos

    def move_position(self, movement):
        self.set_position(self.position + movement)

    def set_momentum(self, new_momentum):
        self.momentum = new_momentum
    
    def set_velocity(self, new_velocity):
        self.momentum = new_velocity
    
    def update(self):
        self.position = self.position + self.velocity

    def draw(self, target):
        pygame.draw.circle(target, self.color, (int(self.position.x), int(self.position.y)), self.radius)
