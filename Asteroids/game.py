import pygame
import random

from color import Color
from coords import Coords
from vec2d import Vec2d
from asteroid import Asteroid
from bullet import Bullet

from player import Player
        
ASTEROID_MIN_RADIUS = 20
ASTEROID_MAX_RADIUS = 40
ASTEROID_DEATH_RADIUS = 5
ASTEROID_WRAP_DISTANCE = 15 # The distance off from the window border that will cause an asteroid to wrap around the screen

LINE_COLOR = Color.WHITE
LINE_COLOR_BACKGROUND = Color.GRAY_2
LINE_THICKNESS = 2
BORDER_THICKNESS = 25

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

        # Game variables
        self.max_asteroid_count = 10
        self.max_background_asteroid_count = 10
        
        # Create the sprite groups
        self.game_objects = pygame.sprite.Group()
        self.asteroid_objects = pygame.sprite.Group()
        self.background_objects = pygame.sprite.Group()
        self.bullet_objects = pygame.sprite.Group()
        
        # Add asteroids
        self.populate_world_with_asteroids()
        
        self.player = Player(Color.WHITE, 15, self.screen, Vec2d(50, 50))

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
                if event.key == pygame.K_SPACE and Bullet.COUNT < 5:
                    Bullet.COUNT = Bullet.COUNT + 1
                    new_bullet = Bullet(
                            Color.WHITE,
                            self.player.rotation,
                            self.player.rotate_point_around_pivot(
                                Vec2d(
                                    self.player.get_real_pos().x,
                                    self.player.get_real_pos().y - self.player.rad
                                ),
                                self.player.get_real_pos(),
                                self.player.rotation
                            ),
                            self.screen
                        )
                    self.bullet_objects.add(new_bullet)

        # --- Drawing code should go here
        # First, clear the screen
        self.screen.fill(self.background_color) 

        # Update and draw BACKGROUND OBJECTS
        for background_obj in self.background_objects:
            background_obj.update(self.dt)
            background_obj.draw(self.screen)
        
        # Update and draw FOREGROUND OBEJCTS
        for obj in self.asteroid_objects: 
            obj.update(self.dt)
            obj.draw(self.screen)
        
        # player collisions
        self.player.update()
        self.wrap_objects()
        self.check_asteroid_collisions(self.asteroid_objects)
        self.check_asteroid_collisions(self.background_objects)

        for bullet in self.bullet_objects:
            bullet.update()
            if bullet.pos.x < 0 or bullet.pos.x > self.screen.get_width() or bullet.pos.y < 0 or bullet.pos.y > self.screen.get_height():
                bullet.kill()
                Bullet.COUNT = Bullet.COUNT - 1
            else:
                bullet.draw()

        # Now, do your drawing.
        self.player.draw()

        # Add game border
        pygame.draw.rect(self.screen, self.background_color, (0, 0, self.width, self.height), 2 * BORDER_THICKNESS)
        pygame.draw.rect(self.screen, LINE_COLOR, (BORDER_THICKNESS, BORDER_THICKNESS, self.width - (2 * BORDER_THICKNESS), self.height - (2 * BORDER_THICKNESS)), LINE_THICKNESS)
        
        # --- Update the screen with what we've drawn.
        pygame.display.update()
    
        # This limits the loop to 60 frames per second
        self.clock.tick(60)
        
    # Adds new asteroids if needed to keep the world full of life!
    def populate_world_with_asteroids(self):
        #print("Asteroid Count: " , len(self.asteroid_objects))
        while len(self.asteroid_objects) < self.max_asteroid_count:
            self.create_random_asteroid()

        while len(self.background_objects) < self.max_background_asteroid_count:
            self.create_random_background_asteroid()
        
    # Creates an asteroid using random parameters
    def create_random_asteroid(self):    
        asteroid_radius = random.randint(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS) 
        asteroid_pos = self.get_random_world_point()
        asteroid_vel = self.get_random_direction() * random.randint(200, 500)
        
        self.create_asteroid(self.asteroid_objects, asteroid_pos, asteroid_vel, asteroid_radius)  
    
    # Creates an asteroid using parameters
    def create_asteroid(self, sprite_group, pos, vel, radius):        
        new_asteroid = Asteroid(pos, vel, radius)
        new_asteroid.set_visual_details(LINE_COLOR, LINE_THICKNESS, self.background_color)
        
        self.game_objects.add(new_asteroid)
        sprite_group.add(new_asteroid)
        
    # Creates an asteroid using random parameters for the background
    def create_random_background_asteroid(self):    
        asteroid_radius = random.randint(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS) 
        asteroid_pos = self.get_random_world_point()
        asteroid_vel = self.get_random_direction() * random.randint(200, 500)
        
        new_asteroid = Asteroid(asteroid_pos, asteroid_vel, asteroid_radius)
        new_asteroid.set_visual_details(LINE_COLOR_BACKGROUND, LINE_THICKNESS, self.background_color)
        
        self.game_objects.add(new_asteroid)
        self.background_objects.add(new_asteroid)
        
    # Gets a random vector on the screen
    def get_random_world_point(self):
        x = random.randint(0, self.width)
        y = random.randint(0, self.height)
        return Vec2d(x, y)
        
    # Gets a random direction
    def get_random_direction(self):
        return Vec2d(random.randint(-1, 1), random.randint(-1, 1)).normalized()
    
    # Removes asteroids that have left the screen
    def wrap_objects(self):
        # For every asteroid... 
        for target_asteroid in self.game_objects:
            # If the asteroid has left the world, wrap it
            if target_asteroid.pos.x < (-ASTEROID_WRAP_DISTANCE): 
                target_asteroid.pos.x = self.width + ASTEROID_WRAP_DISTANCE
            if target_asteroid.pos.x > (self.width + ASTEROID_WRAP_DISTANCE):
                target_asteroid.pos.x = -ASTEROID_WRAP_DISTANCE
            if target_asteroid.pos.y < (-ASTEROID_WRAP_DISTANCE):
                target_asteroid.pos.y = self.height + ASTEROID_WRAP_DISTANCE
            if target_asteroid.pos.y > (self.height + ASTEROID_WRAP_DISTANCE):
                target_asteroid.pos.y = -ASTEROID_WRAP_DISTANCE

    
    # Checks to see if two asteroids are colliding
    def check_asteroid_collisions(self, asteroid_list):
        # For every asteroid in front layer... 
        for target_asteroid in asteroid_list:
            # Make a list without that asteroid to check for collisions
            trimmed_asteroid_objects = pygame.sprite.Group()
            for other_asteroid in asteroid_list:
                if other_asteroid != target_asteroid:
                    trimmed_asteroid_objects.add(other_asteroid)
            
            # Get a list of all other asteroids the target asteroid has collided with
            hits = pygame.sprite.spritecollide(target_asteroid, trimmed_asteroid_objects, False, pygame.sprite.collide_circle)
            if hits:
                for other in hits:
                    target_asteroid.collide_with_asteroid(other)
                    #self.split_asteroid(other)


    # Splits an asteroid into two smaller asteroids
    def split_asteroid(self, asteroid):
        initial_pos = asteroid.pos.copy()
        initial_vel = asteroid.vel.copy()
        initial_speed = initial_vel.get_length()
        new_radius = int(asteroid.radius / 2)
        
        # Remove asteroid from all groups it might be in
        asteroid.kill()
        
        # If the new radius is large enough...
        if new_radius > ASTEROID_DEATH_RADIUS:
            new_pos_1 = Vec2d(initial_pos.x + 50, initial_pos.y)
            self.create_asteroid(new_pos_1, self.get_random_direction() * initial_speed, new_radius)
            self.create_asteroid(initial_pos, self.get_random_direction() * initial_speed, new_radius)


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
