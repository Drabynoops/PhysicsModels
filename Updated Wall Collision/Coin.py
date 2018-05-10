from CollisionObject import CollisionObject
from vec2d import Vec2d

import pygame

class Coin(CollisionObject):

  def __init__(self, points, coords):
    super().__init__(Vec2d(-1.5,2), Vec2d(0,0), 10, points, (255, 255, 0))
    self.drop = False
    self.coords = coords
#    self.type = "coin"

  def update(self, dt):
    if self.drop:
      super().update(dt)
    else:
      mouse_pos = self.coords.pos_to_coords(Vec2d(pygame.mouse.get_pos()))
#      print(mouse_pos.x)
      if mouse_pos.x > 1:
        mouse_pos.x = 0.75
      elif mouse_pos.x < -3.25:
        mouse_pos.x = -3.25
      mouse_pos.y = 2
#      print(mouse_pos)
      self.pos = mouse_pos
  
  def draw(self, screen, coords):
    super().draw(screen, coords)
    points = self.create_draw_points(coords)
    pygame.draw.polygon(screen, (0, 0, 0), points, 2)
  
  def reset(self):
    self.drop = False
    self.vel = Vec2d(0,0)
    self.mom = Vec2d(0,0)
    self.ang_mom = Vec2d(0,0)
    self.angle = 0