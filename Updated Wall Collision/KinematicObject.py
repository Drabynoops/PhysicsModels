from CollisionObject import CollisionObject
from vec2d import Vec2d

class KinematicObject(CollisionObject):
  def __init__(self, pos, vec, density, points, color, e=0, mu=0, angle=0, com_shift=False):
    super().__init__(pos, Vec2d(0, 0), density, points, color, e, mu, angle, 0, com_shift)
    self.type = "kinematic"
    self.moment = 1e99
  
  def update(self, dt):
    pass
  
  def impulse(self, imp, pt):
    pass
