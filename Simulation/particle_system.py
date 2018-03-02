import pygame

class System:

    def __init__(self):
        self.system = []
        self.COUNT = 0
        self.cur_time = pygame.time.get_ticks
        self.last_time = self.cur_time()
    
    def add(self, particle):
        particle.id = self.COUNT
        self.COUNT = self.COUNT + 1
        self.system.append(particle)

    def update(self):
        for i1 in range(len(self.system)):
            for i2 in range(i1):
                    self.system[i1].gravity_force(self.system[i2])
                    self.system[i2].gravity_force(self.system[i1])
        self.last_time = self.cur_time

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
        pass
                    
    
class Particle:

    def __init__(self, radius, pos, mass):
        self.id = None
        self.mass = mass
        self.radius = radius
        self.pos = pos
        self.velocity = 0
        self.GRAVITY = 6.67408**(0 - 11)
    
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
        dt = pygame.time.Clock.get_time() / 1000.0
        #dt = (self.cur_time - self.last_time) / 1000.0
        distance = (self.pos - other.pos).mag() - (self.radius + other.radius) 
        force = (
            (-1 * self.GRAVITY * self.mass * other.mass ) / distance.mag2()
            ) * distance.hat() * dt
        self.velocity = self.velocity + force

    def momentum(self):
        return self.mass * self.velocity