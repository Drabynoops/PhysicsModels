from PhysicsObject import PhysicsObject
from vec2d import Vec2d

class CollisionObject(PhysicsObject):
  def __init__(self, pos, vel, density, points, color, e=0, mu=0, angle=0, angvel=0):
    super().__init__(pos, vel, density, points, color, angle, angvel)
    self.e = e
    self.mu = mu

  
  def check_collision(self, other, result=[]):
    result.clear() # See polygon_collision_test.py in check_collision()
    overlap = 1e99
    collision_normal = Vec2d(0,0)
    # if other.type == "polygon" or other.type == "wall": #Keeping just in case           
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
        if max_d <= 0.0001:
          return False
        else:
          overlap = max_d
          point = self.pos + self.points[max_j]
          collision_normal = n_hat# TODO This is wrong? Which normal is it?
                
    result.extend([self, other, overlap, collision_normal, point])
    return True