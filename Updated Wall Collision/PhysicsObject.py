from Polygon import Polygon
from vec2d import Vec2d
import pygame

class PhysicsObject(Polygon):
  def __init__(self, pos, vel, density, points, color, angle=0, angvel=0, com_shift=True):
    super().__init__(pos, points, color, angle)
    
    self.density = density
    self.vel = vel
    self.angvel = angvel
    self.force = Vec2d(0, 0)
    self.torque = 0
    
    self.area = self.calculate_area()
    self.mass = self.density * self.area
    self.moment = self.calculate_moment()
    
    if com_shift:
      self.shift_around_center_of_mass()

    self.orig_normals = self.calculate_normals(self.orig_points)
    self.initialize_normals(len(self.orig_normals))

    self.update_points_normals()
    self.mom = self.mass * self.vel
    self.angmom  = self.moment * self.angvel
    
    

  def calculate_area(self):
    area = 0
    for i in range(len(self.orig_points)):
      area_triangle = self.orig_points[i-1].cross(self.orig_points[i]) / 2
      area += area_triangle
    return area
  
  def calculate_moment(self):
    center = self.get_center()
    moment_shape = 0
    for i in range(len(self.orig_points)):
      area_triangle = self.orig_points[i-1].cross(self.orig_points[i]) / 2
      moment_shape += (1/6) * self.density * area_triangle * (self.orig_points[i].mag() + self.orig_points[i-1].mag() + self.orig_points[i-1].dot(self.orig_points[i]))
    moment = moment_shape - self.mass * center.mag2() # Parallel Axis Theorem
    return moment

  def shift_around_center_of_mass(self):
    center = self.get_center()
    center_of_mass = self.area * center / self.area
    for p in self.orig_points:
      p -= center_of_mass
    self.pos += center

  def get_center(self):
    center = Vec2d(0, 0)
    for i in range(len(self.orig_points)):
      center += (self.orig_points[i-1] + self.orig_points[i]) / 3
    return center
  
  def calculate_normals(self, points):
    normals = []
    for i in range(len(points)):
      normal = normal = (points[i-1] - points[i]).perpendicular_normal()
      normals.append(normal)
    return normals
  
  def initialize_normals(self, length):
    return self.initialize_points(length)
  
  def update_points_normals(self):
    self.update_points()
    self.normals = self.calculate_normals(self.points)
  
  def update(self, dt):
    self.update_mom(dt)
    self.update_pos(dt)
  
  def update_mom(self, dt):
    self.mom += self.force*dt
    self.angmom += self.torque*dt
    self.update_vel()
    self.update_angvel()

  def update_vel(self):
    self.vel.copy_in(self.mom/self.mass)
  
  def update_angvel(self):
    self.angvel = self.angmom/self.moment

  def update_pos(self, dt):
      self.pos += self.vel*dt
      self.angle += self.angvel*dt
      if self.angvel*dt != 0:
          self.update_points_normals()

  def impulse(self, imp, point=None):
    self.mom += imp
    self.update_vel()
    if point is not None:
      self.angmom += (point - self.pos).cross(imp)
      self.update_angvel()

  def draw(self, screen, coords):
    super().draw(screen, coords)
    points = self.create_draw_points(coords)
    pygame.draw.circle(screen, (0,0,0), coords.pos_to_screen(self.pos).int(), 3)
    if True:
      for i in range(len(points)):
        length = 50
        n = coords.unitvec_to_other(self.normals[i])
        p = (points[i] + points[i-1])/2
        pygame.draw.line(screen, (0,0,0), p, p + length*n)