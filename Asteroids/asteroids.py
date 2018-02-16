import pygame
from pygame import init, quit

from color import Color
from coords import Coords
from vec2d import Vec2d


class Asteroids:

    def __init__(self, width, height):
        pygame.init()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode([width,height])
        self.draw_screen = self.screen.copy()
        self.draw_screen.fill(Color.WHITE)
        self.screen_center = Vec2d(width/2, height/2)
        self.coords = Coords(self.screen_center.copy(), 1, True)

def main():
    input()

    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise 
elif __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise e
