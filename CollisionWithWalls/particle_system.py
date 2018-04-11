import pygame
from vec2d import Vec2d
from enum import Enum
from color import Color
import math
import random

from circle import Circle
from rotating_circle import RotatingCircle
from wall import Wall

class System:

    def __init__(self):
        self.system = []
        self.COUNT = 0
        
        self.collision_checks = 1
        self.system_force = Vec2d(0, -9.8)
        
        self.coefficient_of_friction = 0.05
        self.coefficient_of_restitution = 0.8 #e
        
    def create_circle(self, radius, pos, vel):
        new_circle = RotatingCircle(pos, vel, radius, radius, self.random_color(), Color.BLACK)
        self.system.append(new_circle)
        
        new_circle.id = self.COUNT
        self.COUNT = self.COUNT + 1
        
    def create_wall(self, pos, normal):
        new_wall = Wall(pos, normal, self.random_color())
        self.system.append(new_wall)
        
        new_wall.id = self.COUNT
        self.COUNT = self.COUNT + 1
        
    def random_color(self):
        return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    
    def remove(self, index):
        del self.system[index]
        
    def get(self, index):
        return self.system[index]

    def update(self, dt):
        # Zero the forces
        for i in range(len(self.system)):
            self.system[i].force = Vec2d(0, 0)
            
        # Apply new forces
        for i1 in range(len(self.system)):
            for i2 in range(i1):
                #self.gravity_force(self.system[i1], self.system[i2], dt)
                pass
                
        # Apply system force
        for i in range(len(self.system)):
            self.system[i].force += self.system_force 
            
        # Update physics
        for i in range(len(self.system)):
            self.system[i].update(dt)
            
        # Handle collisions
        for x in range(0, self.collision_checks):
            for i1 in range(len(self.system)):
                for i2 in range(i1):
                    obj_1 = self.system[i1]
                    obj_2 = self.system[i2]
                    
                    # Circle Circle collision
                    if isinstance(obj_1, Circle) and isinstance(obj_2, Circle):
                        if self.detect_collision_circle_circle(obj_1, obj_2):
                            self.collide(obj_1, obj_2)
                    # Wall Circle collision
                    elif isinstance(obj_1, Wall) and isinstance(obj_2, Circle):
                        if self.detect_collision_circle_wall(obj_2, obj_1):
                            #print("Colliding with wall")
                            self.collide_with_wall(obj_2, obj_1)
                    # Circle Wall collision
                    elif isinstance(obj_2, Wall) and isinstance(obj_1, Circle):
                        if self.detect_collision_circle_wall(obj_1, obj_2):
                            #print("Colliding with wall")
                            self.collide_with_wall(obj_1, obj_2)
                        

    def center_system(self, width, height):
        com = self.center_of_mass()
        com_velocity = self.velocity_of_com()
        for particle in self.system:
            particle.velocity = particle.velocity - com_velocity
            particle.pos = (particle.pos - com) + Vec2d(width // 2, height // 2)

    
    def center_of_mass(self):
        if len(self.system) != 0:
            num = 0
            denum = 0
            for particle in self.system:
                num = num + (particle.mass * particle.pos)
                denum = denum + particle.mass
            return num / denum
        else:
            return Vec2d(0, 0)
    
    def velocity_of_com(self):
        num = 0
        denum = 0
        for particle in self.system:
            num = num + particle.momentum()
            denum = denum + particle.mass
        return num / denum 
    
    def draw(self, target, coords):
        for particle in self.system:
            particle.draw(target, coords)
            
    # -------------------
    # Detect a collision \
    # --------------------
    def detect_collision_circle_circle(self, circle_1, circle_2):
        # Calculate distance between objects
        distance_between = (circle_1.pos - circle_2.pos).get_length()
        return (distance_between < (circle_1.radius + circle_2.radius))
    
    # -------------------
    # Detect a collision \
    # --------------------
    def detect_collision_circle_wall(self, obj, wall):
        return (obj.pos - wall.pos).dot(wall.normal) < obj.radius
        
    # --------------------------------------------------
    # Apply collision impulse force between two objects \
    # ---------------------------------------------------
    def collide(self, obj_1, obj_2):
        n_hat = (obj_1.pos - obj_2.pos).hat()                       # Normal vector
        t_hat = n_hat.perpendicular()                               # Vector along the surface (perp of the normal)

        # Depenetrate the objects from each other
        overlap_amount = self.depenetrate_circle_circle(obj_1, obj_2)

        # Difference in velocity along the normal
        v_n = (obj_2.vel - obj_1.vel).dot(n_hat)
        
        # Difference in velocity along the perpendicular of the normal
        v_t =  (obj_2.vel - obj_1.vel).dot(t_hat) - (obj_1.radius * obj_2.ang_vel) - (obj_2.radius * obj_2.ang_vel) # ISSUE WITH ORDERING?

        # --- Bounce Impulse ----------
        reduced_mass_bounce = 1 / ( (1 / obj_1.mass) + (1 / obj_2.mass) )  # Reduced mass
        impulse_bounce = (1 + self.coefficient_of_restitution) * reduced_mass_bounce * v_n # * -1 ???
        
        # --- Friction Impulse --------
        reduced_mass_friction = 1 / (           # !!! MIGHT HAVE ERROR !!!
                (1 / obj_1.mass) + (obj_1.inertia / (obj_1.radius * obj_1.radius)) + 
                (1 / obj_2.mass) + (obj_2.inertia / (obj_2.radius * obj_2.radius)) )

        impulse_friction = -1 * reduced_mass_friction * v_t     # Impulse
        if impulse_friction > (self.coefficient_of_friction * impulse_bounce):
            impulse_friction *= (self.coefficient_of_friction * impulse_bounce / impulse_friction)
        
        # --- Overall Impulse ---------
        impulse = (impulse_bounce * n_hat) + (impulse_friction * t_hat) # SOMETHING IS WRONG WITH FRICTION!!!!!!!!!!!!!!!!
        point_of_impulse = obj_1.pos - (obj_1.radius * n_hat)
        
        obj_1.impulse(impulse, point_of_impulse)
        obj_2.impulse(-1 * impulse, point_of_impulse)
        
        
    # --------------------------------------------------
    # Apply collision impulse force from wall           \
    # ---------------------------------------------------
    def collide_with_wall(self, obj, wall):
        n_hat = wall.normal                                         # Normal vector
        t_hat = n_hat.perpendicular()                               # Vector along the surface (perp of the normal)
        
        reduced_mass = obj.mass                                     # Reduced mass

        # Depenetrate the objects from each other
        overlap_amount = self.depenetrate_circle_wall(obj, wall)
        
        # Difference in velocity along the normal
        v_n = (obj.vel - wall.vel).dot(n_hat)
        
        # Difference in velocity along the perpendicular of the normal (One of the below equations is right...)
        v_t =  (obj.vel - wall.vel).dot(t_hat) - (obj.radius * obj.ang_vel)
                
        # --- Bounce Impulse ----------
        reduced_mass_bounce = obj.mass  # Reduced mass
        impulse_bounce = -1 * (1 + self.coefficient_of_restitution) * reduced_mass_bounce * v_n # * -1 ???
        
        # --- Friction Impulse --------
        reduced_mass_friction = 1 / (           # !!! MIGHT HAVE ERROR !!!
                (1 / obj.mass) + ((obj.radius * obj.radius) / obj.inertia) )

        impulse_friction = -1 * reduced_mass_friction * v_t     # Impulse
        
#        if impulse_friction > (self.coefficient_of_friction * impulse_bounce):
#            impulse_friction *= (reduced_mass_friction * impulse_bounce / impulse_friction)
        
        # --- Overall Impulse ---------
        point_of_impulse = obj.pos - (obj.radius * n_hat)
#        
        impulse = (impulse_bounce * n_hat) + (impulse_friction * t_hat)
        obj.impulse(impulse, point_of_impulse)
        

            
    # --------------------------------------------------
    # Detect collision between a circle and a rectangle \
    # ---------------------------------------------------
    def detect_collision_circle_rect(self, circle, rect):
        delta = self.vector_between_circle_rect(circle, rect)
        #pygame.draw.line(self.screen, Color.GREEN, [circle.pos.x, circle.pos.y], [circle.pos.x - delta.x, circle.pos.y - delta.y], 3)
        return (delta.x * delta.x + delta.y * delta.y) < (circle.radius * circle.radius)
    
    # ------------------------------------------------
    # Returns normal between a circle and a rectangle \
    # -------------------------------------------------
    def vector_between_circle_rect(self, circle, rect):
        rect_x = rect.pos.x - int(rect.width / 2)
        rect_y = rect.pos.y - int(rect.height / 2)
        delta_x = circle.pos.x - max(rect_x, min(circle.pos.x, rect_x + rect.width))
        delta_y = circle.pos.y - max(rect_y, min(circle.pos.y, rect_y + rect.height))
        return Vec2d(delta_x, delta_y)
    
    # -----------------------------
    # Make two objects not overlap \
    # ------------------------------ 
    def depenetrate_circle_circle(self, obj_1, obj_2):
        direction_from_2_to_1 = (obj_1.pos - obj_2.pos).hat()
        direction_from_1_to_2 = (obj_2.pos - obj_1.pos).hat()
        
        # Finds distance of overlap
        dist_between_points = obj_1.radius + obj_2.radius - (obj_1.pos - obj_2.pos).get_length()
        
        # We want to keep the center of mass when moving them apart...
        mu = (obj_1.mass * obj_2.mass) / (obj_1.mass + obj_2.mass)

        # Apply offset to objects
        obj_1.pos += (direction_from_2_to_1 * (dist_between_points * (mu / obj_1.mass)))        
        obj_2.pos += (direction_from_1_to_2 * (dist_between_points * (mu / obj_2.mass)))
        
        return dist_between_points
    
    # -----------------------------
    # Make two objects not overlap \
    # ------------------------------ 
    def depenetrate_circle_wall(self, obj, wall):
        dist_overlap = obj.radius - (obj.pos - wall.pos).dot(wall.normal)
        obj.pos += wall.normal * dist_overlap
        return dist_overlap

    # -----------------------------------
    # Gravity forces from another object \
    # ------------------------------------
    def gravity_force(self, obj_1, obj_2, dt):
        distance = (obj_1.pos - obj_2.pos)
        GRAVITY = 1#6.67408**(0 - 11)
        if (distance.mag() - (obj_1.radius + obj_2.radius)) <= 0:
            #print("No Gravity: Overlapping...")
            # reverse gravity stuff
            force = Vec2d(0, 0)
        else:
            force = ((-1 * GRAVITY * obj_1.mass * obj_2.mass ) / distance.mag2()) * distance.hat()
            obj_1.force += force
            obj_2.force -= force

                   
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
# ==========================================================
# A physics object that uses the properties of an object. 
# ==========================================================
class MyWall:
    
    # ----------------------
    # Initialize the object \
    # -----------------------
    def __init__(self):
        self.id = None
        self.color = Color.RED
        self.thickness = 4
        
        
        #  NORMAL CALCULATION
        # 
        #      normal             B -------- A
        #        ^                     |
        #        |                     v
        #  A -------- B             normal
        
        self.normal = Vec2d(0, 0)
        
        # Physics variables
        self.point_a = Vec2d(0, 0)
        self.point_b = Vec2d(0, 0)
        self.center = Vec2d(0, 0)
        
    # ---------------------------------------
    # Sets basic properties of the wall      \
    # ----------------------------------------
    def set_properties(self, point_a, point_b):
        self.point_a = point_a
        self.point_b = point_b
        
        self.center = Vec2d(int((self.point_a.x + self.point_b.x)/2), int((self.point_a.y + self.point_b.y)/2))
        
        self.normal = (point_b - point_a).perpendicular().hat() * -1
        

    def update(self, dt):
        pass
        
    # --------------------------------
    # Draw the wall to a surface      \
    # ---------------------------------
    def draw(self, surface):
        #print("Wall Normal: ", self.normal)
        pygame.draw.line(surface, self.color, (int(self.point_a.x), int(self.point_a.y)), (int(self.point_b.x), int(self.point_b.y)), self.thickness)
        
        normal_point = (int(self.point_a.x) + int(self.normal.x), int(self.point_a.y) + int(self.normal.y))
        pygame.draw.line(surface, self.color, (int(self.point_a.x), int(self.point_a.y)), normal_point, self.thickness)
        
        
# END OF WALL
# ==========================================================
        
        
        
        
        
        
        
        