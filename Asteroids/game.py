import pygame
import random

from color import Color
from coords import Coords
from vec2d import Vec2d
from asteroid import Asteroid

from player import Player
        
ASTEROID_MIN_RADIUS = 10
ASTEROID_MAX_RADIUS = 30

class Game:

    def __init__(self, width, height):
        pygame.init()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode([width,height])
        self.background_color = Color.BLACK

        self.draw_screen = self.screen.copy()
        self.draw_screen.fill(Color.BLACK)
        self.screen_center = Vec2d(width/2, height/2)
        self.coords = Coords(self.screen_center.copy(), 1, True)
        
        self.dt = 0.001
        self.state = self.play # The game state
        self.done = False
        
        # Create the sprite groups
        self.asteroid_objects = pygame.sprite.Group()
        self.game_objects = pygame.sprite.Group()
        
        # Testing asteroids
        self.create_asteroid(Vec2d(100, 100), Vec2d(400, 400), 2)
        self.create_asteroid(Vec2d(200, 300), Vec2d(-400, -400), 1)
        
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
        self.screen.fill(self.background_color) 
        
        # Now, do your drawing.
        for obj in self.game_objects: 
            obj.update(self.dt)
            obj.draw(self.screen)
        
        self.check_asteroid_collisions()

        # Now, do your drawing.
        self.player.draw(self.screen)
        
        # --- Update the screen with what we've drawn.
        pygame.display.update()
    
        # This limits the loop to 60 frames per second (Modified to 12 fps)
        self.clock.tick(60)
        
    def create_asteroid(self, pos, vel, mass):
        asteroid_radius = random.randint(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS) 
        asteroid_mass = asteroid_radius * asteroid_radius
        new_asteroid = Asteroid(pos, vel, asteroid_mass, asteroid_radius)
        self.game_objects.add(new_asteroid)
        self.asteroid_objects.add(new_asteroid)
        
    def get_random_direction(self):
        return Vec2d(random.randint(-1, 1), random.randint(-1, 1)).normalized()
    
    def check_asteroid_collisions(self):
        # For every asteroid... 
        for target_asteroid in self.asteroid_objects:
            print(target_asteroid.mass)
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

    def run(self):
        pass

def main():
    game = Game(800, 600)
    game.execute_game_loop()

    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise 
