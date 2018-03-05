import pygame
from vec2d import Vec2d
from color import Color

class System:

    def __init__(self):
        self.system = []
        self.COUNT = 0
    
    def add(self, particle):
        particle.id = self.COUNT
        self.COUNT = self.COUNT + 1
        self.system.append(particle)

    def update(self):
        for i1 in range(len(self.system)):
            for i2 in range(i1):
                    self.system[i1].gravity_force(self.system[i2])
                    self.system[i2].gravity_force(self.system[i1])
        for particle in self.system:
            particle.update()

    def center_of_mass(self):
        num = 0
        denum = 0
        for particle in self.system:
            num = num + (particle.mass * particle.pos)
            denum = denum + particle.mass
        return num / denum
    
    def velocity_of_com(self):
        num = 0
        denum = 0
        for particle in self.system:
            num = num + particle.momentum()
            denum = denum + particle.mass
        return num / denum 
    
    def draw(self, target):
        for particle in self.system:
            particle.draw(target)
                    
    
class Particle:

    def __init__(self, radius, pos, mass):
        self.id = None
        self.mass = mass
        self.radius = radius
        self.pos = pos
        self.velocity = 0
        self.GRAVITY = 6.67408**(0 - 11)
        self.last_time = pygame.time.get_ticks()
    
    def __eq__(self, other):
        try:
            if isinstance(other, Particle):
                if self.id == other.id and self.radius == other.radius and self.mass == other.radius and self.pos == self.pos and self.force == self.force:
                    return True
                else:
                    return False
            else:
                raise TypeError
        except TypeError:
            print("Can not compare Particle and non-Particle")

    def gravity_force(self, other):
        cur_time = pygame.time.get_ticks()
        # dt = (cur_time - self.last_time) / 1000.0
        dt = 1 / 60
        self.last_time = cur_time
        distance = (self.pos - other.pos)
        if (distance.mag() - (self.radius + other.radius)) <= 0:
            # reverse gravity stuff
            pass
        force = (
            (-1 * self.GRAVITY * self.mass * other.mass ) / distance.mag2()
            ) * distance.hat() * dt
        self.velocity = self.velocity + force

    def update(self):
        self.pos = self.pos + self.velocity

    def momentum(self):
        return self.mass * self.velocity

    def draw(self, target):
        pygame.draw.circle(target, Color.WHITE, (int(self.pos.x), int(self.pos.y)), self.radius)
