import pygame
from random import uniform, randint, random
from math import sqrt, acos, degrees, sin, cos
from vec2d import Vec2d
from wall import Wall
from coords import Coords
from CollisionObject import CollisionObject

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
GRAY     = ( 127, 127, 127)

def game_settings():
  width = 800
  height = 600
  screen_center = Vec2d(width/2, height/2)
  return [
    pygame.display.set_mode([width,height]),
    Coords(screen_center.copy(), 1, True),
    100,
    60,
    1,
    0.5 # Playback speed
  ]

def create_objects():
  objects = []
  length = 2
  height = 1

  objects.append(CollisionObject(Vec2d(1,2), Vec2d(0,0), 1, make_rectangle(length, height), GRAY, 0, -1))
#  objects.append(CollisionObject(Vec2d(-0.5,3), Vec2d(0,0), 1, make_polygon(0.2,4,0,10), RED, 0, 1))
#  objects.append(CollisionObject(Vec2d(1,0), Vec2d(0,0), 1, make_polygon(0.3,7,0,3), BLUE, 0, -0.4))
#  objects.append(CollisionObject(Vec2d(-1,0), Vec2d(0,0), 1, make_polygon(1,3,0,0.5), GREEN, 0, 2))
  
  # Walls
  objects.append(Wall(Vec2d(-1,-3), Vec2d(1,1), BLACK))
  objects.append(Wall(Vec2d(-1,-3), Vec2d(-1,2), BLACK))
  objects.append(Wall(Vec2d(-1,-4), Vec2d(0,1), BLACK))

  return objects

def random_color():
    return (randint(0,255), randint(0,255), randint(0,255))

def random_bright_color():
    i = randint(0,2)
    d = randint(1,2)
    c = int(256*random()**0.5)
    color = [0,0,0]
    color[i] = 255
    color[(i+d)%3] = c
    return color

def make_polygon(radius, n, angle=0, factor=1, axis=Vec2d(1,0)):
    axis = axis.normalized()
    vec = Vec2d(0, -radius).rotated(180/n+angle)
    p = []
    for i in range(n):
        v = vec.rotated(360*i/n)
        v += v.dot(axis)*(factor-1)*axis
        p.append(v)
    return p

def make_rectangle(length, height, angle=0):
    points = (Vec2d(-0.5,-0.5),
              Vec2d(+0.5,-0.5),
              Vec2d(+0.5,+0.5),
              Vec2d(-0.5,+0.5),
              )
    c = cos(angle)
    s = sin(angle)
    for p in points:
        p.x *= length
        p.y *= height
        x = p.x*c - p.y*s
        y = p.y*c + p.x*s
        p.x = x
        p.y = y
    return points
        
def check_collision(a, b, result=[]):
    result.clear()
    result1 = []
    result2 = []
    if a.check_collision(b, result1) and b.check_collision(a, result2):
        if result1[2] < result2[2]: # compare overlaps, which is smaller
            result.extend(result1)
        else:
            result.extend(result2)
        return True
    return False       

def resolve_collision(result):
    (obj_1, obj_2, overlap, n, pt) = result
    n = n.hat()
    t = n.perpendicular()
    e = 0.0
    mu = 1.0
    reduced_mass = obj_1.mass*obj_2.mass/(obj_1.mass + obj_2.mass) # reduced mass
    
    # depenetrate
    obj_1.pos += (overlap * n)
    obj_1.update_points_normals()

    # distance vectors
    r1 = pt - obj_1.pos # (point of collision - position of object)
    r1n = r1.dot(n)
    r1t = r1.dot(t)
    
    r2 = pt - obj_2.pos 
    r2n = r2.dot(n)
    r2t = r2.dot(t)
    
    # relative velocity of points in contact
    # target velocity change (delta v)
    
    v_rel = (obj_1.vel + (obj_1.angvel * r1.perpendicular())) - (obj_2.vel + (obj_2.angvel * r2.perpendicular()))
    
    delta_Vn = -1 * (1 + e) * v_rel.dot(n)
    delta_Vt = -1 * v_rel.dot(t)
    
    # matrix [[A B][C D]] [Jn Jt]T = [dvn dvt]T
    A = (1 / obj_1.mass) + ((r1t * r1t) / obj_1.moment) + (1 / obj_2.mass) + ((r2t * r2t) / obj_2.moment)
    B = (-1 * (r1n * r1t) / obj_1.moment) * (-1 * (r2n * r2t) / obj_2.moment)
    C = (-1 * (r1n * r1t) / obj_1.moment) * (-1 * (r2n * r2t) / obj_2.moment)
    D = (1 / obj_1.mass) + ((r1n * r1n) / obj_1.moment) + (1 / obj_2.mass) + ((r2n * r2n) / obj_2.moment)
    
    # Solve matrix equation
        # check if friction is strong enough to prevent slipping
        
    if delta_Vn > 0: # If greater than zero, it shouldn't be colliding
        
        Jn = (1 / (A*D - B*C)) * (D*delta_Vn - B*delta_Vt)
        Jt = (1 / (A*D - B*C)) * (-C*delta_Vn + A*delta_Vt)
        
        if abs(Jt) > mu * Jn: # If Jt is too string, recalculate for sliding
            s = 1 if Jt > 0 else -1
            
            Jt = s * mu * Jn
            
            A = (1 / obj_1.mass) + ((r1t * r1t) / obj_1.moment) + (1 / obj_2.mass) + ((r2t * r2t) / obj_2.moment)
            B = (-1 * (r1n * r1t) / obj_1.moment) * (-1 * (r2n * r2t) / obj_2.moment)
            C = -s * mu
            D = 1
            
            Jn = (1 / (A*D - B*C)) * (D*delta_Vn)
        
        J = Jn*n + Jt*t
        obj_1.impulse( J, pt)
        obj_2.impulse(-J, pt)