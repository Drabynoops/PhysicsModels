from math import sin, cos, degrees, radians
from vec2d import Vec2d
import pygame

class Polygon:
  def __init__(self, pos, points, color, angle):
    self.pos = pos
    self.color = color
    self.angle = angle
    self.type = "polygon"

    self.orig_points = self.create_orig_points(points)
    self.points = self.initialize_points(len(self.orig_points))

  def create_orig_points(self, points):
    orig_points = []
    for p in points:
      orig_points.append(p.copy())
    return orig_points

  def initialize_points(self, length):
    points = []
    for i in range(length):
      points.append(Vec2d(0, 0))
    return points
  
  def update_points(self):
    c = cos(self.angle)
    s = sin(self.angle)
    for i in range(len(self.orig_points)):
      point = Vec2d(0, 0)
      point.x = self.orig_points[i].x * c - self.orig_points[i].y * s
      point.y = self.orig_points[i].y * c + self.orig_points[i].x * s
      self.points[i] = point
  
  def draw(self, screen, coords):
    points = self.create_draw_points(coords)
    pygame.draw.polygon(screen, self.color, points)
  
  def create_draw_points(self, coords):
    points = []
    for p in self.points:
      points.append(coords.pos_to_screen(self.pos + p))
    return points