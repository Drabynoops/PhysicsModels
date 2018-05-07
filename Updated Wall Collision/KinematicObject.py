from CollisionObject import CollisionObject

class KinematicObject(CollisionObject):
  def __init__(self, pos, vel, density, points, color, e=0, mu=0, angle=0, angvel=0):
    super().__init__(pos, vel, density, points, color, e, mu, angle, angvel)
    self.type = "kinematic"
    self.moment = 1e99
  
  def update(self, dt):
    pass
  
  def impulse(self, imp, pt):
    pass
