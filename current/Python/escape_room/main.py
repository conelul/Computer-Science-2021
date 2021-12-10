#!/usr/bin/env python3.10

import pretty_errors, sys, pygame as pg
from pygame.locals import *
from games import *
from pathlib import Path

pretty_errors.configure(
    separator_character = '*',
    filename_display = pretty_errors.FILENAME_FULL,
    lines_before=10,
    code_color = pretty_errors.default_config.line_color,
    stack_depth=2,
    exception_file_color=pretty_errors.BRIGHT_BLUE
)

CURRENT_DIR = Path(sys.executable if getattr(sys, 'frozen', False) else __file__).resolve().parent

def load_image(name: str) -> pg.Surface: # Simple function to load image from assets/ with image name
    return pg.image.load(CURRENT_DIR / 'assets' / 'images' / name)

#                 R    G    B
RED =           (155,   0,   0)
GREEN =         (  0, 155,   0)
BLUE =          (  0,   0, 155)
YELLOW =        (155, 155,   0)
LIGHTGREY =     (150, 150, 150)


SCALE = 2
FPS = 60
WINWIDTH = 1000 * SCALE
WINHEIGHT = 600 * SCALE

SIMULATE_GAME_SOLUTION = (RED, GREEN, BLUE, YELLOW)
SLIDE_PUZZLE_IMAGE = load_image('seven.png')

class Button(object):
    def __init__(self, image: pg.Surface, size: tuple = None):
        # Scale image if there's an image, also define image rect if there's an image
        if size:
            self.image = pg.transform.scale(image, size)
            self.image_rect = image.get_rect()
        else:
            self.image = image
            self.image_rect = image.get_rect()
            
    def draw(self, location: tuple = (0, 0)):
        self.image_rect.topleft = location
        DISPLAYSURF.blit(self.image, self.image_rect)
    
    def highlight(self):
        pass
        
def main():
    global FPSCLOCK, FPS, DISPLAYSURF, BACKGROUND, MEMORY_GAME_BUTTON, SIMULATE_GAME_BUTTON, SLIDE_PUZZLE_BUTTON, BASICFONT, LOCK_BUTTON
    
    pg.init()
    FPSCLOCK = pg.time.Clock() # FPS clock
    DISPLAYSURF = pg.display.set_mode((WINWIDTH, WINHEIGHT), pg.SCALED) # Screen obj
    pg.display.set_caption('Escape Room') # Window title
    BASICFONT = pg.font.Font('freesansbold.ttf', 32) # Font
    
    # Load images
    BACKGROUND = pg.transform.scale(load_image('background.png'), (WINWIDTH, WINHEIGHT))
    MEMORY_GAME_IMAGE = load_image('triangle_three.png')

    # Load buttons
    MEMORY_GAME_BUTTON = Button(load_image('memory_game_icon.png'), (50 * SCALE, 30 * SCALE))
    SIMULATE_GAME_BUTTON = Button(load_image('simulate_game_icon.png'), (50 * SCALE, 50 * SCALE))
    SLIDE_PUZZLE_BUTTON = Button(load_image('sliding_puzzle_icon.png'), (50 * SCALE, 50 * SCALE))
    LOCK_BUTTON = Button(load_image('lock.png'), (50 * SCALE, 30 * SCALE))
    
    # Load games and game info
    SLIDE_PUZZLE = SlidePuzzle(SLIDE_PUZZLE_IMAGE, DISPLAYSURF, (WINWIDTH/2 - 540, WINHEIGHT/2 - 540), (500 * SCALE, 500 * SCALE), 80 * SCALE, 240)
    SIMULATE_GAME = SimulateGame(SIMULATE_GAME_SOLUTION, DISPLAYSURF, (WINWIDTH/2 - 540, WINHEIGHT/2 - 540), (500 * SCALE, 500 * SCALE))
    MEMORY_GAME = MemoryGame(MEMORY_GAME_IMAGE, (5, 4), DISPLAYSURF, (WINWIDTH/2 - 540, WINHEIGHT/2 - 540), (500 * SCALE, 500 * SCALE), 150)
    
    playing = False
    lock_opened = False
    
    while True: # Game loop
        draw_background()
        if lock_opened: draw_lock((400 * SCALE, 100 * SCALE), (0, 0))
        for event in pg.event.get(): # Event handling
            if event.type == QUIT:
                terminate()
            elif event.type == MOUSEBUTTONUP: # Mouse pressed
                if SLIDE_PUZZLE_BUTTON.image_rect.collidepoint(event.pos) and not playing:
                    # Load and play the slide puzzle game
                    playing = True
                    playing = SLIDE_PUZZLE.play(playing)
                elif SIMULATE_GAME_BUTTON.image_rect.collidepoint(event.pos) and not playing:
                    playing = True
                    playing = SIMULATE_GAME.play(playing)
                elif MEMORY_GAME_BUTTON.image_rect.collidepoint(event.pos) and not playing:
                    playing = True
                    playing = MEMORY_GAME.play(playing)
                elif LOCK_BUTTON and not playing:
                    lock_opened = True       
        pg.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pg.quit()
    sys.exit(0)

def draw_background():
        # Display background
        DISPLAYSURF.blit(BACKGROUND, (0, 0))
        
        # Display back button and game buttons
        MEMORY_GAME_BUTTON.draw((.325 * WINWIDTH, .685 * WINHEIGHT))
        SIMULATE_GAME_BUTTON.draw((.7 * WINWIDTH, .75 * WINHEIGHT))
        SLIDE_PUZZLE_BUTTON.draw((.1 * WINWIDTH, .75 * WINHEIGHT))
        LOCK_BUTTON.draw((.4 * WINWIDTH, .685 * WINHEIGHT))

def draw_lock(size: tuple[int], location: tuple[int]):
    lock_bg = pg.Surface(size)
    lock_bg.fill(LIGHTGREY)
    DISPLAYSURF.blit(lock_bg, (0, 0))

if __name__ == '__main__':
    main()