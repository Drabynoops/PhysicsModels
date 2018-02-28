import pygame

class System:

    def __init__(self):
        self.system = []
        self.COUNT = 0
        self.GRAVITY = 6.67408**(0 - 11)
        self.cur_time = pygame.time.get_ticks
        self.last_time = self.cur_time()
    
    def add(self, particle):
        particle.id = self.COUNT
        self.COUNT = self.COUNT + 1
        self.system.append(particle)
    
    def gravity_force(self, particle_one, particle_two):
        dt = pygame.time.Clock.get_time() / 1000.0
        #dt = (self.cur_time - self.last_time) / 1000.0
        distance = particle_one.pos - particle_two.pos
        force = (
            (-1 * self.GRAVITY * particle_one.mass * particle_two.mass ) / distance.mag2()
            ) * distance.hat() * dt
        particle_one.force = particle_one.force + force
        particle_two.force = particle_two.force - force

    def update(self):
        for i1 in range(len(self.system)):
            for i2 in range(i1):
                    self.gravity_force(self.system[i1], self.system[i2])
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
                    
    
class Particle:

    def __init__(self, radius, pos, mass):
        self.id = None
        self.mass = mass
        self.radius = radius
        self.pos = pos
        self.velocity = 0
    
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

    def momentum(self):
        return self.mass * self.velocity