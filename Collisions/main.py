import pygame
from random import randint

from color import Color
from circle import Circle
from wall import Wall
from vec2d import Vec2d
from coords import Coords

class Game:

    def __init__(self, width, height):
        self.game_objects = []
        self.coords = Coords(Vec2d(width/2, height/2))

        pygame.init()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode([width, height])
        self.background_color = Color.BLACK
        self.gravity = Vec2d(0, 9.8)

        self.draw_screen = self.screen.copy()
        self.draw_screen.fill(Color.BLACK)

        self.done = False
        self.state = self.run

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

        self.build_game_objects()

    def build_game_objects(self):
        self.generate_circles()
        self.game_objects.append(Wall(Vec2d(-100, 200), Vec2d(-1, 1), Color.WHITE))
        self.game_objects.append(Wall(Vec2d(100, 200), Vec2d(1, 1), Color.WHITE))
    
    def generate_circles(self):
        max_x = self.height / 2
        min_x = 100 
        min_y = -self.width / 2
        max_y = self.width / 2
        min_radius = 5
        max_radius = 25
        for i in range(5):
            radius = randint(min_radius, max_radius)
            self.game_objects.append(Circle(Vec2d(randint(min_x, max_x), randint(min_y, max_y)), Vec2d(0,0), radius * 1.5, radius, Color.BLUE))
    
    def execute_game_loop(self):
        while not self.done:
            self.state()
        pygame.quit()
    
    def run(self):
        # dt = ( 1 / self.clock.get_time() ) if self.clock.get_time() is not 0 else ( 1 / 60 )
        dt = 1 / 60
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If user clicked close
                self.done = True
        
        # First, clear the screen
        self.screen.fill(self.background_color)

        for index in range(len(self.game_objects)):
            obj = self.game_objects[index]
        # Update velocity stuffs
            if obj.type == "circle":
                obj.force = obj.force + (self.gravity * dt)
                obj.update(dt)

                # Collision stuffs
                for index_2 in range( index + 1, len(self.game_objects) ):
                    obj_2 = self.game_objects[index_2]
                    if obj.type == "circle" and obj_2.type == "circle":
                        obj.collide_with_circle(obj_2)
                        obj.update(dt)
                        obj_2.update(dt)
                    elif obj.type == "circle" and obj_2.type == "wall":
                        obj.collide_with_wall(obj_2)  
                        obj.update(dt)      
        # Update stuff
            obj.update(dt)
        # Draw stuff
            obj.draw(self.screen, self.coords)

        # --- Update the screen with what we've drawn.
        pygame.display.update()

        # This limits the loop to 60 frames per second
        self.clock.tick(60)

def main():
    game = Game(800, 600)
    game.execute_game_loop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise
