# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 13:56:44 2017

@author: sinkovitsd
"""
import pygame
from vec2d import Vec2d
from collision_system_functions import game_settings, create_objects, , check_collision, resolve_collision, WHITE, make_circle
from TextElement import TextElement
from Interpolation import Interpolation, test_callback, update_interpolation_list
from Coin import Coin

def main():
  pygame.init()
 
  # Get all basic game settings
  (screen, coords, zoom, frame_rate, n_per_frame, playback_speed) = game_settings()
  coords.zoom_at_coords(Vec2d(0,0), zoom) 
  
  # Score
  score = 0

  # Used to manage how fast the screen updates
  clock = pygame.time.Clock()
  
  font_style_1 = pygame.font.SysFont('Calibri', 40, True, False) # (font, size, bold, italics)
  font_style_2 = pygame.font.SysFont('Calibri', 60, False, False) # (font, size, bold, italics)
  font_style_3 = pygame.font.SysFont('Calibri', 16, True, False) # (font, size, bold, italics)
  font_style_4 = pygame.font.SysFont('Calibri', 16, False, False) # (font, size, bold, italics)
  
  # Create UI...
  ui_elements = [
    TextElement(font_style_1, Vec2d(-3, 3.2), "Plinko", 0.0, 0.5), 
    TextElement(font_style_4, Vec2d(-3, 2.9), "Keenan Barber & Brendan Bard", 0.0, 0.5), 
    
    TextElement(font_style_2, Vec2d(2.25, 2.0), "000", 0.5, 0.5), 
    TextElement(font_style_1, Vec2d(2.25, 1.5), "SCORE", 0.5, 0.5), 
    
    TextElement(font_style_3, Vec2d(1.2, 0.5), "ATTEMPTS LEFT:", 0.0, 0.5),
    TextElement(font_style_2, Vec2d(3.3, 0.5), "00", 1.0, 0.5),
    
    TextElement(font_style_3, Vec2d(1.2, 0.0), "COINS DROPPED:", 0.0, 0.5),
    TextElement(font_style_2, Vec2d(3.3, 0.0), "00", 1.0, 0.5),
  ]

  # Create initial objects
  objects = create_plinko_board()
  
  coin = Coin(make_circle(32, 0.125), coords)
  # coin = Coin(make_rectangle(0.25, 0.25), coords)
  objects.append(coin)

  # Interpolation Array
  interpolations = []
  # Test Interpolation
  interpolations.append(Interpolation(Interpolation.linear_equation, 0, 5, test_callback, None, 5.0))

  # -------- Main Program Loop -----------\
  dt = playback_speed/frame_rate/n_per_frame
  done = False
  paused = True
  max_collisions = 1
  result = []
  while not done:
    
    # --- Handle Input ------
    # Update to coords...
#    mouse_pos = Vec2d(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
#    mouse_pos = (mouse_pos - Vec2d((int)(screen.get_width()/2), (int)(screen.get_height/2)))/zoom 
#    mouse_pos.y *= -1
    
    # --- Main event loop
    for event in pygame.event.get(): 
      if event.type == pygame.QUIT: # If user clicked close
        done = True
        paused = True
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if paused:
          paused = False
        else:
          coin.drop = True
      elif event.type == pygame.KEYDOWN: 
        if event.key == pygame.K_ESCAPE:
          done = True
          paused = True 
        elif event.key == pygame.K_SPACE:
          paused = not paused
        else:
          paused = False
    
    if not paused:
      
      # # Update the existing interpolations
      # update_interpolation_list(interpolations, dt)
      
      for N in range(n_per_frame):
        # Physics
        # Calculate the force on each object
        for obj in objects:
          obj.force.zero()
          obj.force += Vec2d(0,-10) # gravity
   
        # Move each object according to physics
        for obj in objects:
          obj.update(dt)
            
        for i in range(max_collisions):
          collided = False
          for i1 in range(len(objects)):
            for i2 in range(i1):
              if check_collision(objects[i1], objects[i2], result):
                resolve_collision(result)
                collided = True
          if not collided: # if all collisions resolved, then we're done
            break
 
    # Drawing
    screen.fill(WHITE) # wipe the screen
    pygame.draw.line(screen, BLACK, coords.pos_to_screen(Vec2d(-3, 2)), coords.pos_to_screen(Vec2d(3, 2)), 3)
    for obj in objects:
      obj.draw(screen, coords) # draw object to screen

    # UI
    for i in range(len(ui_elements)):
      ui_elements[i].draw(screen, coords)

    # --- Update the screen with what we've drawn.
    pygame.display.update()
    
    # This limits the loop to the specified frame rate
    clock.tick(frame_rate)
      
  pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        pygame.quit()
        raise
