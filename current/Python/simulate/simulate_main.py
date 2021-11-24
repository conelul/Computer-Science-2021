#!/usr/bin/env python3.10
import sys, pygame, simulate_modified as sim
from pygame.locals import *
# All this code does is create a button calle "Play"
# If you click that button, it calls the simulate game main function from the module, as a demonstration that it can be used in the escape room.
# Only issue is that it creates a new window (which isn't that bad, but it's different from what i planned)

#                R    G    B
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
BRIGHTRED    = (255,   0,   0)
RED          = (155,   0,   0)
BRIGHTGREEN  = (  0, 255,   0)
GREEN        = (  0, 155,   0)
BRIGHTBLUE   = (  0,   0, 255)
BLUE         = (  0,   0, 155)
BRIGHTYELLOW = (255, 255,   0)
YELLOW       = (155, 155,   0)
DARKGRAY     = ( 40,  40,  40)

sequence = (RED, RED) # CORRECT SEQUENCE
# initializing the constructor
pygame.init()
  
# screen resolution
res = (480, 480)
screen = pygame.display.set_mode(res)


width = screen.get_width()
height = screen.get_height()
  
FONT = pygame.font.Font(pygame.font.get_default_font(),35)
  
result_text = None
result = None

def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = FONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)
      
PLAY_SURF, PLAY_RECT = makeText('Play', WHITE, None, res[0]/2.5, (res[1]/2)-50)

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif ev.type == pygame.MOUSEBUTTONDOWN and PLAY_RECT.collidepoint(ev.pos):
            result = sim.main(sequence,(res[0],res[1]))
            result_text = FONT.render(result, True, WHITE)

    screen.fill((60,25,60))
    screen.blit(PLAY_SURF, PLAY_RECT)
    
    if result_text:
        screen.blit(result_text, (res[0]/2.5, res[1]/2))

    # updates the frames of the game
    pygame.display.update()
