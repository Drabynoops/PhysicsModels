# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:26:03 2018

@author: sinkovitsd
"""

from math import sin, cos, degrees, radians
from vec2d import Vec2d
import pygame

class Polygon:
    def __init__(self, pos, vel, density, points, color, angle=0, angvel=0):
        self.pos = pos
        self.vel = vel
        self.color = color
        self.angle = angle
        self.angvel = angvel
        self.force = Vec2d(0,0)
        self.torque = 0
        self.density = density
        self.type = "polygon"

        # Set origpoints
        self.origpoints = []
        for p in points:
            self.origpoints.append(p.copy())
        pp = self.origpoints # pp as an alternate label for this function
        # print('Points', points)
        # Tally area, moment, and center of mass
        self.area = 0
        self.moment = 0
        moment_shape = 0
        center = Vec2d(0,0)
        for i in range(len(pp)):
            # TODO area of triangle, and add to total area
            area_triangle = pp[i-1].cross(pp[i])/2
            self.area += area_triangle
            # TODO moment of triange about vertex
            moment_shape += (1/6) * self.density * area_triangle * (pp[i].mag() + pp[i-1].mag() + pp[i-1].dot(pp[i]))
            # TODO add center of mass of triange to center of mass of shape
            center += area_triangle * (pp[i] + pp[i-1]) / 3
            pass
        center *= 1/self.area
        self.mass = density*self.area
        print("center =", center)
        print("area =", self.area)
        print("mass =", self.mass)

        # Shift self.origpoints to be centered on center of mass
        for p in self.origpoints:
            p -= center
        self.pos += center
        
        #TODO Shift moment to be about center of mass (parallel axis theorem)
        #   o Calculate the moment for each triangle and put the sum of them all into moment_shape
        self.moment = moment_shape - self.mass * center.mag2() # Parallel Axis Theorem

        print("moment =", self.moment)

        # Recalculate moment around the center of mass as a check
        moment = 0
        for i in range(len(pp)):
            # TODO same as above loop to tally moment of each triangle about vertex
            # TODO area of triangle, and add to total area
            area_triangle = pp[i-1].cross(pp[i])/2
            # TODO moment of triange about vertex
            moment += (1/6) * self.density * area_triangle * (pp[i].mag() + pp[i-1].mag() + pp[i-1].dot(pp[i]))
            pass
        print("moment =", moment)
        
        # Calculate normals to each points
        self.orignormals = []
        for i in range(len(pp)):
            #TODO calculate normal here and append to orignormals
            normal = (pp[i-1] - pp[i]).perpendicular_normal()
            self.orignormals.append(normal)
        print("orignormals =", self.orignormals)
        
        # Calculate rotated points and normals
        self.points = []
        for p in self.origpoints:
            self.points.append(Vec2d(0, 0))
        self.normals = []
        for n in self.orignormals:
            self.normals.append(Vec2d(0, 0))
        self.update_points_normals()
                
        self.mom = self.mass*self.vel
        self.angmom = self.moment*self.angvel
        print("points =", self.points)
        print("normals =", self.normals)
        
    def update_mom(self, dt):
        self.mom += self.force*dt
        self.angmom += self.torque*dt
        self.update_vel()
        self.update_angvel()
        
    def set_vel(self, vel):
        self.vel.copy_in(vel)
        self.mom.copy_in(self.vel*self.mass)

    def update_vel(self):
        self.vel.copy_in(self.mom/self.mass)
    def update_angvel(self):
        self.angvel = self.angmom/self.moment

    def update_pos(self, dt):
        self.pos += self.vel*dt
        self.angle += self.angvel*dt
        if self.angvel*dt != 0:
            self.update_points_normals()
            
    def update_points_normals(self):
        c = cos(self.angle)
        s = sin(self.angle)
        for i in range(len(self.origpoints)):
            point = Vec2d(0,0)
            point.x = self.origpoints[i].x * c - self.origpoints[i].y * s
            point.y = self.origpoints[i].y * c + self.origpoints[i].x * s
            self.points[i] = point
        for i in range(len(self.points)):
            normal = (self.points[i-1] - self.points[i]).perpendicular_normal()
            self.normals[i] = normal
        #TODO use s and c to calculate points and normals rotated

    def update(self, dt):
        self.update_mom(dt)
        self.update_pos(dt)
                
    def impulse(self, imp, point=None):
        self.mom += imp
        self.update_vel()
        if point is not None:
            self.angmom += (point - self.pos).cross(imp)  
            self.update_angvel()

    def draw(self, screen, coords):
        # Draw polygon
        points = []
        for p in self.points:
            points.append(coords.pos_to_screen(self.pos + p))
        pygame.draw.polygon(screen, self.color, points)
        if True:
            for i in range(len(points)):
                length = 50
                n = coords.unitvec_to_other(self.normals[i])
                p = (points[i] + points[i-1])/2
                pygame.draw.line(screen, (0,0,0), p, p + length*n)
                
                
    def check_collision(self, other, result=[]):
        result.clear() # See polygon_collision_test.py in check_collision()
        overlap = 1e99
        collision_normal = Vec2d(0,0)
        if other.type == "polygon":            
            """ Self supplies the vertices.  Other provides the sides (walls).
                For each wall, find the point that penetrates the MOST, 
                and record the magnitude of penetration.  If for one wall, 
                no point penetrates, there is no overlap; return False.
                Otherwise, find which wall is LEAST penetrated, and pass back,
                via result.extend(), the overlap, point and normal involved; 
                return True. """
            for i in range(len(other.normals)):
                max_d = -1e99
                max_j = -1
                n_hat = Vec2d(0, 0)
                r_other = other.pos + other.points[i]
                normal = other.normals[i]
                for j in range(len(self.points)):
                    r_self = self.pos + self.points[j]
                    distance = (r_other - r_self).dot(normal)
                    if distance > max_d:
                        max_d = distance
                        max_j = j
                        n_hat = normal
                if max_d < overlap:
                    if max_d <= 0.1:
                        return False
                    else:
                        overlap = max_d
                        point = self.pos + self.points[max_j]
                        collision_normal = n_hat# TODO This is wrong? Which normal is it?
            result.extend([self, other, overlap, collision_normal, point])
            return True

    
    