# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 13:56:44 2017

@author: sinkovitsd
"""
import pygame
from vec2d import Vec2d

class Circle:
    def __init__(self, pos, vel, mass, radius, color):
        self.pos = pos.copy()
        self.mass = mass
        self.radius = radius
        self.vel = vel.copy()
        self.mom = self.vel*self.mass
        self.color = color
        self.force = Vec2d(0,0)
        self.type = "circle"
        self.col_restituion = 0.5
    
    def update_mom(self, dt):
        self.mom += self.force*dt
        self.update_vel()
    
    def set_mom(self, new_mom):
        self.mom = new_mom
        self.update_vel()
    
    def set_vel(self, vel):
        self.vel.copy_in(vel)
        self.mom.copy_in(self.vel*self.mass)

    def update_vel(self):
        self.vel.copy_in(self.mom/self.mass)

    def update_pos(self, dt):
        self.pos += self.vel*dt

    def update(self, dt):
        self.update_mom(dt)
        self.update_pos(dt)

    def collide_with_circle(self, other):
        pos1 = self.pos
        pos2 = other.pos

        r1 = self.radius
        r2 = other.radius

        m1 = self.mass
        m2 = other.mass

        v1 = self.vel
        v2 = other.vel

        distance = (pos1 - pos2).mag()

        if distance < ( r1 + r2 ) :
            penetration_distance = (r1 + r2) - distance
            reduced_mass = ( m1 * m2 ) / ( m1 + m2 )
            normal = ( pos1 - pos2 ) / (pos1 - pos2).mag()

            self.pos = pos1 + ( ( reduced_mass * penetration_distance ) / m1 ) * normal
            other.pos = pos2 - ( ( reduced_mass * penetration_distance ) / m2 ) * normal

            collision_impulse = -( 1 + self.col_restituion ) * reduced_mass * ( v1 - v2 ).dot( normal ) * normal
            
            angular_momentum = (reduced_mass * distance * normal.perpendicular()).dot((v1 - v2))
            rotational_impulse = (-distance / (distance * (distance + penetration_distance))) * angular_momentum * normal.perpendicular()

            if (v1 - v2).dot(normal) < 0:
                self.set_mom(self.mom + collision_impulse + rotational_impulse)
                other.set_mom(other.mom - collision_impulse - rotational_impulse)
            return True
        else:
            return False

    def collide_with_wall(self, other):
        distance = -(self.pos - other.pos).dot(other.normal) - self.radius
        if distance < 0:
            reduced_mass = self.mass
            normal = other.normal

            # ( reduced_mass * distance ) / self.mass
            # Since reduced_mass = self.mass this means distance
            self.pos += (reduced_mass * distance) * normal

            impulse = -(1 + self.col_restituion) * reduced_mass * (self.vel - other.vel).dot(normal) * normal
            '''I have no idea what is going on here.
               I only hope that this is correct.
               Nothing seems to break so yea?
            '''
            velocity_normal = ((-normal.dot(self.vel)) / self.vel.mag2()) * self.vel #vn
            velocity_tangential = ((-normal.perpendicular().dot(self.vel)) / self.vel.mag2()) * self.vel #vn
            impulse_normal = -(1 + self.col_restituion) * reduced_mass * velocity_normal.mag() * normal #Jn
            max_friction = other.friction_coefficient * impulse_normal
            impulse_friction = -other.friction_coefficient * velocity_tangential.mag() * normal.perpendicular()
            if impulse_friction.mag2() > max_friction.mag2():
                impulse_friction *= (other.friction_coefficient * impulse_normal.mag()) / impulse_friction.mag()
            '''End of the madness'''
            self.set_mom(self.mom + impulse + impulse_friction)
            return True
        else:
            return False

    def draw(self, screen, coords):
        pygame.draw.circle(screen, self.color, 
                           coords.pos_to_screen(self.pos).int(), 
                           int(coords.scalar_to_screen(self.radius)+0.5), 0)
 