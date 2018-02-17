import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self, color, radius, pos=None):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        self.pos = pos if pos else [0, 0]
        self.radius = radius
        self.color = color

        self.set_hidden_values()
        self.create_image()

    def set_hidden_values(self):
        self.__local_pos = [self.radius, self.radius]
        self.__global_pos = [self.pos[0] -
                             self.radius, self.pos[1] - self.radius]

    def create_image(self):
        # Addition is cheaper than multiplication
        self.__image = pygame.Surface(
            [self.radius + self.radius, self.radius + self.radius])
        pygame.draw.circle(self.__image, self.color,
                           self.__local_pos, self.radius)

    def move_pos(self, move_vector):
        self.__global_pos[0] += move_vector[0]
        self.__global_pos[1] += move_vector[1]

    def draw(self, target):
        target.blit(self.__image, self.__global_pos)
