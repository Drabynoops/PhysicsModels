import pygame

from color import Color
from collision_circle import CollisionCircle
from wall import Wall
from vec2d import Vec2d

class Game:

    def __init__(self, width, height):
        self.game_objects = []

        pygame.init()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode([width, height])
        self.background_color = Color.BLACK

        self.draw_screen = self.screen.copy()
        self.draw_screen.fill(Color.BLACK)

        self.done = False
        self.state = self.run

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

        self.build_game_objects()

    def build_game_objects(self):
        self.game_objects.append(CollisionCircle(10, Vec2d(250, 250), 0))
        self.game_objects.append(CollisionCircle(10, Vec2d(500, 250), 0))
        self.game_objects.append(Wall(Vec2d(0, 300), Vec2d(400, 600)))
        self.game_objects.append(Wall(Vec2d(400, 600), Vec2d(800, 300)))
    
    def execute_game_loop(self):
        while not self.done:
            self.state()
        pygame.quit()
    
    def run(self):
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If user clicked close
                self.done = True
        
        # First, clear the screen
        self.screen.fill(self.background_color)

        for o in range(len(self.game_objects)):
            obj = self.game_objects[o]
            if isinstance(obj, CollisionCircle):
                obj.move_position(Vec2d(0, 1))
                for i in range(o, len(self.game_objects)):
                    obj2 = self.game_objects[i]
                    if isinstance(obj2, CollisionCircle):
                        obj.collide_with_circle(obj2)
                    else:
                        obj.collide_with_wall(obj2)

            obj.update()
            obj.draw(self.screen)
            

        
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
