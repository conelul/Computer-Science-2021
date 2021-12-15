#!/usr/bin/env python3.10

import sys, pygame as pg
from pygame.locals import *
from games import *
from pathlib import Path
from pygame import mixer


CURRENT_DIR = Path(sys.executable if getattr(sys, 'frozen', False) else __file__).resolve().parent

def load_image(name: str) -> pg.Surface: # Simple function to load image from assets/ with image name
    return pg.image.load(CURRENT_DIR / 'assets' / 'images' / name)

#                 R    G    B
RED =           (155,   0,   0)
GREEN =         (  0, 155,   0)
BLUE =          (  0,   0, 155)
YELLOW =        (155, 155,   0)
LIGHTGREY =     (150, 150, 150)
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)

SCALE = 2 # Scales only the background, NOT THE GAMES
FPS = 60
WINWIDTH = 1000 * SCALE
WINHEIGHT = 600 * SCALE

SIMULATE_GAME_SOLUTION = (RED, GREEN, BLUE, YELLOW)
SLIDE_PUZZLE_IMAGE = load_image('seven.png')

CODE = "743"

class Button(object):
    def __init__(self, image: pg.Surface, size: tuple = None):
        # Scale image if there's an image, also define image rect if there's an image
        if size:
            self.image = pg.transform.scale(image, size)
            self.image_rect = self.image.get_rect()
        else:
            self.image = image
            self.image_rect = self.image.get_rect()
            
    def draw(self, location: tuple = (0, 0)):
        self.image_rect.topleft = location
        DISPLAYSURF.blit(self.image, self.image_rect)

def makeText(text, color, bgcolor, top, left):
        # create the Surface and Rect objects for some text.
        textSurf = BASICFONT.render(text, True, color, bgcolor)
        textRect = textSurf.get_rect()
        textRect.topleft = (top, left)
        return (textSurf, textRect)
        
def main():
    global FPSCLOCK, FPS, DISPLAYSURF, BACKGROUND, MEMORY_GAME_BUTTON, SIMULATE_GAME_BUTTON, REPLAY_SURF, REPLAY_RECT, SLIDE_PUZZLE_BUTTON, BASICFONT, SEQUENCE, LOCK_BUTTON, WRONG_SOUND, INPUT_RECT, LOCK_CLOSE_SURF, LOCK_CLOSE_RECT, user_text, SUBMIT_SURF, SUBMIT_RECT
    
    pg.init()
    FPSCLOCK = pg.time.Clock() # FPS clock
    DISPLAYSURF = pg.display.set_mode((WINWIDTH, WINHEIGHT), pg.RESIZABLE) # Screen obj
    pg.display.set_caption('Escape Room') # Window title
    BASICFONT = pg.font.Font('freesansbold.ttf', 50) # Font
    
    mixer.init()
    
    mixer.music.load(f'{CURRENT_DIR}/assets/sounds/song.mp3')
    mixer.music.set_volume(.05)
    mixer.music.play()
    
    OPEN_SOUND = pg.mixer.Sound(f'{CURRENT_DIR}/assets/sounds/paper2.mp3')
    OPEN_SOUND.set_volume(.3)
    
    WRONG_SOUND = pg.mixer.Sound(f'{CURRENT_DIR}/assets/sounds/wrong.mp3')
    WRONG_SOUND.set_volume(.3)
    
    # Lock screen setup
    submits = 0
    user_text = "" # Text in the lock input box
    INPUT_RECT = pg.Rect(WINWIDTH / 2 - 200 * SCALE, WINHEIGHT / 2 - 150 * SCALE, 400 * SCALE, 300 * SCALE)
    input_active = False
    LOCK_CLOSE_SURF, LOCK_CLOSE_RECT = makeText('Close', WHITE, BLACK, WINWIDTH / 2 + 40 * SCALE, WINHEIGHT / 2 + 100 * SCALE + 20) # Close button for the lock
    SUBMIT_SURF, SUBMIT_RECT = makeText('Submit', WHITE, BLACK, WINWIDTH / 2 - 90 * SCALE, WINHEIGHT / 2 + 100 * SCALE + 20) # Close button for the lock
    SEQUENCE = pg.transform.scale(load_image('sequence.png'), (400, 120))
    REPLAY_SURF, REPLAY_RECT = makeText('Restart', BLUE, BLACK, WINWIDTH/2 - 75, WINHEIGHT/2 + 100) # Close button for the lock

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
    
    game_over = False
    playing = False
    lock_opened = False
    while True: # Game loop
        draw_background()
        if game_over: 
            restart_screen()
            lock_opened = False
            
        if lock_opened: 
            draw_lock()
            
        for event in pg.event.get(): # Event handling
            if event.type == QUIT:
                terminate()
            if event.type == MOUSEBUTTONUP: # Mouse pressed
                if SLIDE_PUZZLE_BUTTON.image_rect.collidepoint(event.pos) and not playing:
                    # Load and play the slide puzzle game
                    playing = True
                    OPEN_SOUND.play()
                    playing = SLIDE_PUZZLE.play(playing)
                elif SIMULATE_GAME_BUTTON.image_rect.collidepoint(event.pos) and not playing:
                    playing = True
                    OPEN_SOUND.play()
                    playing = SIMULATE_GAME.play(playing)
                elif MEMORY_GAME_BUTTON.image_rect.collidepoint(event.pos) and not playing:
                    playing = True
                    OPEN_SOUND.play()
                    playing = MEMORY_GAME.play(playing)
                elif LOCK_BUTTON.image_rect.collidepoint(event.pos) and not playing:
                    playing = True
                    lock_opened = True
                    OPEN_SOUND.play()
                # Lock input 
                if INPUT_RECT.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False
                # Close/Submit buttons for the lock
                if SUBMIT_RECT.collidepoint(event.pos) and lock_opened:
                    game_over = check_code(user_text)
                    user_text = ""
                elif LOCK_CLOSE_RECT.collidepoint(event.pos) and lock_opened:
                    playing = False
                    lock_opened = False
                if REPLAY_RECT.collidepoint(event.pos) and game_over:
                    main()
            if event.type == KEYDOWN:
                if event.key == pg.K_BACKSPACE and input_active:
                    user_text = user_text[:-1] # Delete one character if del pressed
                elif input_active and len(user_text) <=2: # Only allow 3 or fewer characters
                        user_text += event.unicode
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

def draw_lock():
    # Draw the actual lock
    pg.draw.rect(DISPLAYSURF, LIGHTGREY, INPUT_RECT)
    font = pg.font.Font('freesansbold.ttf', 300)
    input_message = BASICFONT.render("Enter the code here:", True, WHITE)
    text_surface = font.render(user_text, True, (255, 255, 255))
    
    DISPLAYSURF.blit(input_message, (INPUT_RECT.x+5, INPUT_RECT.y+5))
    DISPLAYSURF.blit(text_surface, (INPUT_RECT.x + 160, INPUT_RECT.y+75)) # Display the lock
    DISPLAYSURF.blit(SEQUENCE, (INPUT_RECT.x+220, INPUT_RECT.y+350))
    
    DISPLAYSURF.blit(LOCK_CLOSE_SURF, LOCK_CLOSE_RECT) # Draw close button for the lock
    DISPLAYSURF.blit(SUBMIT_SURF, SUBMIT_RECT) # Draw submit button for the lock
    # Update
    pg.display.flip()
    FPSCLOCK.tick(FPS)

def check_code(code):
    if code == CODE:
        restart_screen()
        return True
    elif code != "":
        WRONG_SOUND.play()
        return False

def restart_screen():
    pg.mixer.pause()
    DISPLAYSURF.fill(BLACK)
        
    text_surf = BASICFONT.render("You solved the puzzles and escaped!", True, WHITE)
    credits_surf = BASICFONT.render("Made by Conor S.", True, WHITE)
    
    DISPLAYSURF.blit(text_surf, (WINWIDTH/2 - text_surf.get_width()/2 , WINHEIGHT/2 - text_surf.get_height()/2))
    DISPLAYSURF.blit(credits_surf, (WINWIDTH/2 - text_surf.get_width()/2 + 250, WINHEIGHT/2 - text_surf.get_height()/2 + 60))
    
    DISPLAYSURF.blit(REPLAY_SURF, REPLAY_RECT)
    pg.display.update()

if __name__ == '__main__':
    main()