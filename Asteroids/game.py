import pygame

from color import Color
from coords import Coords
from vec2d import Vec2d
from player import Player
from asteroid import Asteroid
        

class Game:

    def __init__(self, width, height):
        pygame.init()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode([width,height])
        self.draw_screen = self.screen.copy()
        self.draw_screen.fill(Color.BLACK)
        self.screen_center = Vec2d(width/2, height/2)
        self.coords = Coords(self.screen_center.copy(), 1, True)
        
        self.state = self.play # The game state
        self.done = False
        
        self.player = Player(Color.WHITE, 15, [50, 50])

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()
        
    def execute_game_loop(self):
        # -------- Main Program Loop -----------\
        while not self.done:
            self.state()
            
        pygame.quit()
        
    def play(self):
        # --- Main event loop
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: # If user clicked close
                self.done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.move_pos([0, -1])
                elif event.key == pygame.K_DOWN:
                    self.player.move_pos([0, 1])
                elif event.key == pygame.K_LEFT:
                    self.player.move_pos([-1, 0])
                elif event.key == pygame.K_RIGHT:
                    self.player.move_pos([1, 0])

        # --- Drawing code should go here
        # First, clear the screen
        self.screen.fill(Color.BLACK) 
        
        # Now, do your drawing.
        self.player.draw(self.screen)
        
        # --- Update the screen with what we've drawn.
        pygame.display.update()
    
        # This limits the loop to 60 frames per second (Modified to 12 fps)
        self.clock.tick(60)

    def run(self):
        pass

def main():
    game = Game(400, 300)
    game.execute_game_loop()

    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise 
