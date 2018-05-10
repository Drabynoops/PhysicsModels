from KinematicObject import KinematicObject
from vec2d import Vec2d

class Bumper(KinematicObject):

  def __init__(self, score, pos, vec, density, points, color, e=0, mu=0, angle=0, com_shift=False):
    super().__init__(pos, Vec2d(0, 0), density, points, color, e, mu, angle, com_shift)

    self.type = "kinematic"
    self.score = score