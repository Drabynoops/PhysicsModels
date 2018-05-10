import pygame
from random import uniform, randint, random
from math import sqrt, acos, degrees, sin, cos
from vec2d import Vec2d
from wall import Wall
from coords import Coords
from CollisionObject import CollisionObject
from KinematicObject import KinematicObject
from Trigger import Trigger
from Coin import Coin

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
GRAY     = ( 127, 127, 127)

THEME_COLOR_1 = (74, 172, 214)
THEME_COLOR_2 = (55, 130, 163)
THEME_COLOR_DETAILS = WHITE

BOARD_WIDTH = 300
BOARD_PADDING = 10

def random_color():
  return (randint(0,255), randint(0,255), randint(0,255))

def game_settings():
  width = 800
  height = 750
  screen_center = Vec2d(width/2, height/2)
  return [
    pygame.display.set_mode([width,height]),
    Coords(screen_center.copy(), 1, True),
    100, # zoom
    60, # frame rate
    1, # n per frame
    1 # Playback speed
  ]

def create_objects():
  objects = []
  length = 2
  height = 1

  objects.append(CollisionObject(Vec2d(0,2), Vec2d(0,0), 1, make_rectangle(length, height), GRAY, 0, 1, 0.3, 0.8))
  objects.append(KinematicObject(Vec2d(1,0), Vec2d(0,0), 1, make_rectangle(4, height), GRAY, 0, 1, 0.2))
  
#  objects.append(KinematicObject(Vec2d(0.5,0), Vec2d(0,0), 1, make_polygon(0.2,4,0,10), RED, 0.3, 0.8, -0.2, 0))
#  objects.append(CollisionObject(Vec2d(1,0), Vec2d(0,0), 1, make_polygon(0.3,7,0,3), BLUE, 0.3, 0.8))
#  objects.append(CollisionObject(Vec2d(-1,0), Vec2d(0,0), 1, make_polygon(1,3,0,0.5), GREEN, 0.3, 0.8))
  
  # Walls
  #pos, normal, color, e=0, mu=0
  objects.append(Wall(Vec2d(-1,-3), Vec2d(1,1), BLACK, 0.3, 0.7))
  objects.append(Wall(Vec2d(-1,-3), Vec2d(-1,2), BLACK, 0.3, 0.7))
  objects.append(Wall(Vec2d(-1,-4), Vec2d(0,1), BLACK, 0.3, 0.7))

  return objects

def create_plinko_board():
  objects = []
  length = 2
  height = 1

#  objects.append(CollisionObject(Vec2d(0,2), Vec2d(0,0), 1, make_rectangle(length, height), GRAY, 0, 1, 0.3, 0.8))
#  objects.append(KinematicObject(Vec2d(1,0), Vec2d(0,0), 1, make_right_triangle(-45, 0.5), RED, 0, 1, 0))

  # Walls (pos, normal, color, e=0, mu=0)
  
#  PEG_COUNT = 10
#  PEG_ROWS = 4
#  peg_start_x = -3.5
#  peg_spacing = 4.5 / PEG_COUNT
#  for x in range(0, PEG_COUNT + 1):
#    for y in range(0, PEG_ROWS):
#      
#      if (x + y) % 2 == 0: # Even
#        
#      else: # Odd
#        
#      
#    # Peg
#    objects.append(KinematicObject(Vec2d(peg_start_x + (x * peg_spacing),0), Vec2d(0,0), 0.2, make_polygon(1,10,0,1,Vec2d(1,0),0.1), RED, 0, 1, 0))
  
  # Right Ramp
  objects.append(KinematicObject(Vec2d(1,-3), Vec2d(0,0), 1, make_right_triangle(-45, 1.0), GRAY, 0, 1, 0))
  # Left Ramp
  objects.append(KinematicObject(Vec2d(-3.5,-3), Vec2d(0,0), 1, make_right_triangle(45, 1.0), GRAY, 0, 1, 0))
  
  
  # Left Wall
  objects.append(Wall(Vec2d(-3.5, 0), Vec2d(1, 0), BLACK, 0.3, 0.7))
  # Right Wall
  objects.append(Wall(Vec2d(1.0, 0), Vec2d(-1, 0), BLACK, 0.3, 0.7))
  # Top Wall
  objects.append(Wall(Vec2d(0,2.5), Vec2d(0,-1), BLACK, 0.3, 0.7))
  # Bottom Wall
#  objects.append(Wall(Vec2d(0,-3.75), Vec2d(0,1), BLACK, 0.3, 0.7))

  return objects

def create_pinball_objects():
  objects = []
  length = 2
  height = 1

  objects.append(CollisionObject(Vec2d(0,2), Vec2d(0,0), 1, make_rectangle(length, height), GRAY, 0, 1, 0.3, 0.8))
#  objects.append(KinematicObject(Vec2d(1,0), Vec2d(0,0), 1, make_right_triangle(-45, 0.5), RED, 0, 1, 0))
#  objects.append(KinematicObject(Vec2d(-1,0), Vec2d(0,0), 1, make_right_triangle(45, 0.5), GREEN, 0, 1, 0))

#  objects.append(Bumper(50, Vec2d(1,0), Vec2d(0,0), 1, make_rectangle(length, height), RED, 3, 0, 0))
  # objects.append(KinematicObject(Vec2d(-1,0), Vec2d(0,0), 1, make_right_triangle(45, 0.5), GREEN, 0, 1, 0))
#  objects.append(KinematicObject(Vec2d(0.5,0), Vec2d(0,0), 1, make_polygon(0.2,4,0,10), RED, 0.3, 0.8, -0.2, 0))
#  objects.append(CollisionObject(Vec2d(1,0), Vec2d(0,0), 1, make_polygon(0.3,7,0,3), BLUE, 0.3, 0.8))
#  objects.append(CollisionObject(Vec2d(-1,0), Vec2d(0,0), 1, make_polygon(1,3,0,0.5), GREEN, 0.3, 0.8))
  
  # Walls
  #pos, normal, color, e=0, mu=0
  objects.append(Wall(Vec2d(-3, 0), Vec2d(1, 0), BLACK, 0.7, 0.3))
  objects.append(Wall(Vec2d(3, 0), Vec2d(-1, 0), BLACK, 0.7, 0.3))
  objects.append(Wall(Vec2d(0, -3), Vec2d(0, 1), BLACK, 0.3, 0.7))

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

def make_circle(num_points, radius):
  points = []

  base_vector = Vec2d(radius, 0)
  degree_diff = 360 / num_points

  for i in range(num_points):
    points.append(base_vector.rotated(degree_diff * i))
  
  return points  

def make_right_triangle(hypot_angle, width=1, point_offset=Vec2d(0, 0)):
  
  if hypot_angle >= 90 or hypot_angle <= -90:
    return ()
  
  facing_right = True if hypot_angle < 0 else False
  direction = -1 if facing_right else 1
  hypot_angle = abs(hypot_angle)
  
  deg2rad = (3.1415 / 180)
  x_unit_circle = cos(hypot_angle * deg2rad)
  y_unit_circle = sin(hypot_angle * deg2rad)
#  print("Triangle:", x_unit_circle, ",", y_unit_circle)
  
  y_val = width * (y_unit_circle / x_unit_circle) # Similar triangles
  
  points = (Vec2d(-width / 2, 0),
            Vec2d(+width / 2, 0),
            Vec2d((-width/2) * direction, y_val)
            )
  
  auto_offset = Vec2d(direction*(width/2), 0)
  for p in points:
    p += point_offset + auto_offset

  return points
  
def make_flipper(angle=0, scale=1):
  points = (Vec2d(-1.5,-0.25),
            Vec2d(+1,-0.25),
            Vec2d(+1.25,0.0),
            Vec2d(+1.25,0.25),
            Vec2d(+1,+0.5),
            Vec2d(-1.75,+0.25),
            )
  
  return points

def make_polygon(radius, n, angle=0, factor=1, axis=Vec2d(1,0), scale=1):
    axis = axis.normalized()
    vec = Vec2d(0, -radius).rotated(180/n+angle)
    p = []
    for i in range(n):
        v = vec.rotated(360*i/n)
        v += v.dot(axis)*(factor-1)*axis
        p.append(v)
        
    for point in p:
      point *= scale
    
    return p

def make_rectangle(length, height, angle=0):
    points = (Vec2d(-0.5,-0.5),
              Vec2d(+0.5,-0.5),
              Vec2d(+0.5,+0.5),
              Vec2d(-0.5,+0.5)
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
            
        if result[0].type == "trigger":
          result[0].callback()
          return False
        
        elif result[1].type == "trigger":
          result[1].callback()
          return False
            
        if (result[0].type == "kinematic"):
          temp = result[0]
          result[0] = result[1]
          result[1] = temp
          result[3] = result[3] * -1
          
        return True
    return False       

def resolve_collision(result):
    (obj_1, obj_2, overlap, n, pt) = result
    n = n.hat()
    t = n.perpendicular()
    e = obj_2.e
    mu = obj_2.mu
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