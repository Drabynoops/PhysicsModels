import pygame
from pygame import init, quit
import math
import random

from color import Color
from coords import Coords
from vec2d import Vec2d
from asteroid import Asteroid

BACKGROUND_COLOR = (0, 0, 0)

class Game:

    def __init__(self, width, height):
        pygame.init()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode([width,height])
        self.screen_center = Vec2d(width/2, height/2)
        self.coords = Coords(self.screen_center.copy(), 1, True)
        
        self.dt = 0.001
        self.state = self.play # The game state
        self.done = False
        
        # Create the sprite groups
        self.asteroid_objects = pygame.sprite.Group()
        self.game_objects = pygame.sprite.Group()
        
        # Testing asteroids
        test_asteroid_1 = Asteroid(Vec2d(60, 60), Vec2d(100, 100), 1)
        test_asteroid_2 = Asteroid(Vec2d(300, 300), Vec2d(-500, -500), 1)
        
        self.game_objects.add(test_asteroid_1)
        self.game_objects.add(test_asteroid_2)
        self.asteroid_objects.add(test_asteroid_1)
        self.asteroid_objects.add(test_asteroid_2)
        
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
            
        # --- Drawing code should go here
        # First, clear the screen
        self.screen.fill(( 0, 0, 0)) 
        
        # Now, do your drawing.
        for obj in self.game_objects: 
            obj.update(self.dt)
            obj.draw(self.screen)
        
        self.check_asteroid_collisions()
        
        # --- Update the screen with what we've drawn.
        pygame.display.update()
    
        # This limits the loop to 60 frames per second (Modified to 12 fps)
        self.clock.tick(60)
        
    def get_random_direction(self):
        return Vec2d(random.randint(-1, 1), random.randint(-1, 1)).normalized()
    
    def check_asteroid_collisions(self):
        # For every asteroid... 
        for target_asteroid in self.asteroid_objects:
            
            # Make a list without that asteroid to check for collisions
            trimmed_asteroid_objects = pygame.sprite.Group()
            for other_asteroid in self.asteroid_objects:
                if other_asteroid != target_asteroid:
                    trimmed_asteroid_objects.add(other_asteroid)
            
            # Get a list of all other asteroids the target asteroid has collided with
            hits = pygame.sprite.spritecollide(target_asteroid, trimmed_asteroid_objects, False, pygame.sprite.collide_circle)
            if hits:
                for other in hits:
                    target_asteroid.collide_with_asteroid(other)
                    #sprite.kill()
    
    # Not tested yet
    def split_asteroid(self, asteroid):
        initial_pos = asteroid.pos.copy()
        initial_vel = asteroid.vel.copy()
        initial_speed = initial_vel.get_length()
        
        # Remove asteroid from all groups it might be in
        asteroid.kill()
        
        new_asteroid_1 = Asteroid(initial_pos, self.get_random_direction() * initial_speed, 1)
        new_asteroid_2 = Asteroid(initial_pos, self.get_random_direction() * initial_speed, 1)
        
        self.game_objects.add(new_asteroid_1)
        self.game_objects.add(new_asteroid_2)
        self.asteroid_objects.add(new_asteroid_1)
        self.asteroid_objects.add(new_asteroid_2)

def main():
    game = Game(800, 600)
    game.execute_game_loop()

    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise 
