#!/usr/bin/env python3.10
# Games for the escape room.
# ALL GAMES ORIGINALLY BY AL SWEIGART, UNDER THE SIMPLIFIED BSD LICENSE

import sys, random, time, pygame as pg
from pathlib import Path

# Colors
#                 R    G    B
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
GREEN =         (  0, 204,   0)
LIGHTPINK =     (255, 100, 175)
LIGHTGREY =     (150, 150, 150)
LIGHTBLUE =     (0  , 191, 255)
WHITE =         (255, 255, 255)
BLACK =         (  0,   0,   0)
BRIGHTRED =     (255,   0,   0)
RED =           (155,   0,   0)
BRIGHTGREEN =   (  0, 255,   0)
GREEN =         (  0, 155,   0)
BRIGHTBLUE =    (  0,   0, 255)
BLUE =          (  0,   0, 155)
BRIGHTYELLOW =  (255, 255,   0)
YELLOW =        (155, 155,   0)
DARKGRAY =      ( 40,  40,  40)
GRAY =          (100, 100, 100)
ORANGE =        (255, 128,   0)
PURPLE =        (255,   0, 255)
CYAN =          (  0, 255, 255)

CURRENT_DIR = Path(sys.executable if getattr(sys, 'frozen', False) else __file__).resolve().parent

class Game(object):
    def __init__(self, dest_surf: pg.Surface, location: tuple[int], size: tuple[int], fps: int=60):
        self.LOCATION = location
        self.DEST = dest_surf
        
        self.WINDOWWIDTH = size[0]
        self.WINDOWHEIGHT = size[1]
        self.FPS = fps
        self.FPSCLOCK = pg.time.Clock()
        self.DISPLAYSURF = pg.Surface((self.WINDOWWIDTH, self.WINDOWHEIGHT))
        
    def terminate(self):
        pg.quit()
        sys.exit()
        
    def checkForQuit(self):
        for event in pg.event.get(pg.QUIT): # get all the QUIT events
            self.terminate() # terminate if any QUIT events are present
        for event in pg.event.get(pg.KEYUP): # get all the KEYUP events
            if event.key == pg.K_ESCAPE:
                self.terminate() # terminate if the KEYUP event was for the Esc key
            pg.event.post(event) # put the other KEYUP event objects back
            
    def makeText(self, text, color, bgcolor, top, left):
        # create the Surface and Rect objects for some text.
        textSurf = self.BASICFONT.render(text, True, color, bgcolor)
        textRect = textSurf.get_rect()
        textRect.topleft = (top, left)
        return (textSurf, textRect)

    def update(self):
        self.DEST.blit(self.DISPLAYSURF, self.LOCATION)
        pg.display.update()
        self.FPSCLOCK.tick(self.FPS)


class SlidePuzzle(Game):
    def __init__(self, image, dest_surf, location: tuple[int], size: tuple[int], tilesize: int=50, fps: int=60):
        super().__init__(dest_surf, location, size, fps)
        self.TILESIZE = tilesize
        self.BOARDWIDTH = 4  # number of columns in the board
        self.BOARDHEIGHT = 4 # number of rows in the board
        self.IMAGE = pg.transform.scale(image, (self.TILESIZE * self.BOARDWIDTH, self.TILESIZE * self.BOARDHEIGHT)) # Scale image to fit the puzzle
        
        # Coloring and font
        self.TILECOLOR = LIGHTBLUE
        self.TEXTCOLOR = WHITE
        self.BORDERCOLOR = BLACK
        self.BUTTONCOLOR = WHITE
        self.BUTTONTEXTCOLOR = BLACK
        self.MESSAGECOLOR = WHITE
        self.BASICFONT = pg.font.Font('freesansbold.ttf', 45)
        self.BGCOLOR = LIGHTGREY
        
        # Behavior
        self.BLANK = None
        self.UP = 'up'
        self.DOWN = 'down'
        self.LEFT = 'left'
        self.RIGHT = 'right'
        
        # Margins
        self.XMARGIN = int((self.WINDOWWIDTH - (self.TILESIZE * self.BOARDWIDTH + (self.BOARDWIDTH - 1))) / 2)
        self.YMARGIN = int((self.WINDOWHEIGHT - (self.TILESIZE * self.BOARDHEIGHT + (self.BOARDHEIGHT - 1))) / 2)
        
        # Store the option buttons and their rectangles in OPTIONS.
        self.QUIT_SURF, self.QUIT_RECT = self.makeText('Close', self.TEXTCOLOR, GREEN, self.WINDOWWIDTH - 200, self.WINDOWHEIGHT - 90)
    
        # Generate board
        self.mainBoard, self.solutionSeq = self.generateNewPuzzle(80)

    def play(self, playing: bool) -> bool: # Main game loop
        self.SOLVEDBOARD = self.getStartingBoard() # a solved board is the same as the board in a start state.
        allMoves = [] # list of moves made from the solved configuration
        
        while playing: # main game loop
            slideTo = None # the direction, if any, a tile should slide
            msg = 'Click tile or press arrow keys to slide.' # contains the message to show in the upper left corner.
            if self.mainBoard == self.SOLVEDBOARD:
                msg = 'Solved!'

            self.drawBoard(self.mainBoard, msg)


            self.checkForQuit()
            for event in pg.event.get(): # event handling loop
                if event.type == pg.MOUSEBUTTONUP:
                    spotx, spoty = self.getSpotClicked(self.mainBoard, event.pos[0], event.pos[1])

                    if (spotx, spoty) == (None, None):
                          # check if the user clicked on an option button
                        if self.QUIT_RECT.collidepoint((event.pos[0] - self.LOCATION[0], event.pos[1] - self.LOCATION[1])):
                            return False
                            allMoves = []
                    else:
                        # check if the clicked tile was next to the blank spot
                        blankx, blanky = self.getBlankPosition(self.mainBoard)
                        if spotx == blankx + 1 and spoty == blanky:
                            slideTo = self.LEFT
                        elif spotx == blankx - 1 and spoty == blanky:
                            slideTo = self.RIGHT
                        elif spotx == blankx and spoty == blanky + 1:
                            slideTo = self.UP
                        elif spotx == blankx and spoty == blanky - 1:
                            slideTo = self.DOWN

                elif event.type == pg.KEYUP:
                    # check if the user pressed a key to slide a tile
                    if event.key in (pg.K_LEFT, pg.K_a) and self.isValidMove(self.mainBoard, self.LEFT):
                        slideTo = self.LEFT
                    elif event.key in (pg.K_RIGHT, pg.K_d) and self.isValidMove(self.mainBoard, self.RIGHT):
                        slideTo = self.RIGHT
                    elif event.key in (pg.K_UP, pg.K_w) and self.isValidMove(self.mainBoard, self.UP):
                        slideTo = self.UP
                    elif event.key in (pg.K_DOWN, pg.K_s) and self.isValidMove(self.mainBoard, self.DOWN):
                        slideTo = self.DOWN

            if slideTo:
                self.slideAnimation(self.mainBoard, slideTo, 'Click tile or press arrow keys to slide.', 8) # show slide on screen
                self.makeMove(self.mainBoard, slideTo)
                allMoves.append(slideTo) # record the slide
                
            self.update()
    
    def getStartingBoard(self):
        # Return a board data structure with tiles in the solved state.
        # For example, if BOARDWIDTH and BOARDHEIGHT are both 3, this function
        # returns [[1, 4, 7], [2, 5, 8], [3, 6, BLANK]]
        counter = 1
        board = []
        for x in range(self.BOARDWIDTH):
            column = []
            for y in range(self.BOARDHEIGHT):
                column.append(counter)
                counter += self.BOARDWIDTH
            board.append(column)
            counter -= self.BOARDWIDTH * (self.BOARDHEIGHT - 1) + self.BOARDWIDTH - 1

        board[self.BOARDWIDTH-1][self.BOARDHEIGHT-1] = self.BLANK
        return board
    
    def getBlankPosition(self, board):
        # Return the x and y of board coordinates of the blank space.
        for x in range(self.BOARDWIDTH):
            for y in range(self.BOARDHEIGHT):
                if board[x][y] == self.BLANK:
                    return (x, y)
        
    def makeMove(self, board, move):
        # This function does not check if the move is valid.
        blankx, blanky = self.getBlankPosition(board)

        if move == self.UP:
            board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
        elif move == self.DOWN:
            board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
        elif move == self.LEFT:
            board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
        elif move == self.RIGHT:
            board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]

    def isValidMove(self, board, move):
        blankx, blanky = self.getBlankPosition(board)
        return (move == self.UP and blanky != len(board[0]) - 1) or \
            (move == self.DOWN and blanky != 0) or \
            (move == self.LEFT and blankx != len(board) - 1) or \
            (move == self.RIGHT and blankx != 0)

    def getRandomMove(self, board, lastMove=None):
        # start with a full list of all four moves
        validMoves = [self.UP, self.DOWN, self.LEFT, self.RIGHT]

        # remove moves from the list as they are disqualified
        if lastMove == self.UP or not self.isValidMove(board, self.DOWN):
            validMoves.remove(self.DOWN)
        if lastMove == self.DOWN or not self.isValidMove(board, self.UP):
            validMoves.remove(self.UP)
        if lastMove == self.LEFT or not self.isValidMove(board, self.RIGHT):
            validMoves.remove(self.RIGHT)
        if lastMove == self.RIGHT or not self.isValidMove(board, self.LEFT):
            validMoves.remove(self.LEFT)

        # return a random move from the list of remaining moves
        return random.choice(validMoves)

    def getLeftTopOfTile(self, tileX, tileY):
        left = self.XMARGIN + (tileX * self.TILESIZE) + (tileX - 1)
        top = self.YMARGIN + (tileY * self.TILESIZE) + (tileY - 1)
        return (left, top)

    def getSpotClicked(self, board, x, y):
        # from the x & y pixel coordinates, get the x & y board coordinates
        for tileX in range(len(board)):
            for tileY in range(len(board[0])):
                left, top = self.getLeftTopOfTile(tileX, tileY)
                tileRect = pg.Rect(left, top, self.TILESIZE + self.LOCATION[0], self.TILESIZE + self.LOCATION[1])
                if tileRect.collidepoint(x, y):
                    return (tileX, tileY)
        return (None, None)

    def drawTile(self, tilex, tiley, number, adjx=0, adjy=0):
        # draw a tile at board coordinates tilex and tiley, optionally a few
        # pixels over (determined by adjx and adjy)
        left, top = self.getLeftTopOfTile(tilex, tiley)
        xpos = ((number - 1)% 4)*self.TILESIZE # x coord of image
        ypos = ((number - 1) // 4)*self.TILESIZE # y coord of image
        self.DISPLAYSURF.blit(self.IMAGE, (left + adjx, top + adjy), (xpos, ypos, self.TILESIZE, self.TILESIZE))
        textSurf = self.BASICFONT.render(str(number), True, self.TEXTCOLOR)
        textRect = textSurf.get_rect()
        textRect.center = left + int(self.TILESIZE / 6) + adjx, top + int(self.TILESIZE/1.2) + adjy # bottom left corner
        self.DISPLAYSURF.blit(textSurf, textRect)

    def drawBoard(self, board, message):
        self.DISPLAYSURF.fill(self.BGCOLOR)
        if message:
            textSurf, textRect = self.makeText(message, self.MESSAGECOLOR, self.BGCOLOR, 5, 5)
            self.DISPLAYSURF.blit(textSurf, textRect)

        for tilex in range(len(board)):
            for tiley in range(len(board[0])):
                if board[tilex][tiley]:
                    self.drawTile(tilex, tiley, board[tilex][tiley])

        left, top = self.getLeftTopOfTile(0, 0)
        width = self.BOARDWIDTH * self.TILESIZE
        height = self.BOARDHEIGHT * self.TILESIZE
        pg.draw.rect(self.DISPLAYSURF, self.BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

        self.DISPLAYSURF.blit(self.QUIT_SURF, self.QUIT_RECT)

    def slideAnimation(self, board, direction, message, animationSpeed):
        # Note: This function does not check if the move is valid.

        blankx, blanky = self.getBlankPosition(board)
        if direction == self.UP:
            movex = blankx
            movey = blanky + 1
        elif direction == self.DOWN:
            movex = blankx
            movey = blanky - 1
        elif direction == self.LEFT:
            movex = blankx + 1
            movey = blanky
        elif direction == self.RIGHT:
            movex = blankx - 1
            movey = blanky

        # prepare the base surface
        self.drawBoard(board, message)
        baseSurf = self.DISPLAYSURF.copy()
        # draw a blank space over the moving tile on the baseSurf Surface.
        moveLeft, moveTop = self.getLeftTopOfTile(movex, movey)
        pg.draw.rect(baseSurf, self.BGCOLOR, (moveLeft, moveTop, self.TILESIZE, self.TILESIZE))
        
        for i in range(0, self.TILESIZE, animationSpeed):
            # animate the tile sliding over
            self.checkForQuit()
            self.DISPLAYSURF.blit(baseSurf, (0, 0))
            if direction == self.UP:
                self.drawTile(movex, movey, board[movex][movey], 0, -i)
            if direction == self.DOWN:
                self.drawTile(movex, movey, board[movex][movey], 0, i)
            if direction == self.LEFT:
                self.drawTile(movex, movey, board[movex][movey], -i, 0)
            if direction == self.RIGHT:
                self.drawTile(movex, movey, board[movex][movey], i, 0)

            self.update()

    def generateNewPuzzle(self, numSlides):
        # From a starting configuration, make numSlides number of moves (and
        # animate these moves).
        sequence = []
        board = self.getStartingBoard()
        self.drawBoard(board, '')
        pg.display.update()
        lastMove = None
        for i in range(numSlides):
            move = self.getRandomMove(board, lastMove)
            self.makeMove(board, move)
            sequence.append(move)
            lastMove = move
        return (board, sequence)

        
class SimulateGame(Game):
    def __init__(self, correct_sequence: tuple[str], dest_surf: pg.Surface, location: tuple[int], size: tuple[int], fps: int=60):
        super().__init__(dest_surf, location, size, fps)
        self.CORRECT_SEQUENCE = correct_sequence
        self.FLASHSPEED = 500 # in milliseconds
        self.FLASHDELAY = 200 # in milliseconds
        self.BUTTONGAPSIZE = self.WINDOWWIDTH / 36 # Scaled gap size
        self.TIMEOUT = 4 # seconds before game over if no button is pushed.
        self.bgColor = BLACK
        
        # Button size in px
        self.BUTTONSIZE = (self.WINDOWWIDTH-40)/2
        
        # Margins
        self.XMARGIN = int((self.WINDOWWIDTH - (2 * self.BUTTONSIZE) - self.BUTTONGAPSIZE) / 2)
        self.YMARGIN = int((self.WINDOWHEIGHT - (2 * self.BUTTONSIZE) - self.BUTTONGAPSIZE) / 2)
        
        # Rect objects for each of the four buttons
        self.YELLOWRECT = pg.Rect(self.XMARGIN, self.YMARGIN, self.BUTTONSIZE, self.BUTTONSIZE)
        self.BLUERECT   = pg.Rect(self.XMARGIN + self.BUTTONSIZE + self.BUTTONGAPSIZE, self.YMARGIN, self.BUTTONSIZE, self.BUTTONSIZE)
        self.REDRECT    = pg.Rect(self.XMARGIN, self.YMARGIN + self.BUTTONSIZE + self.BUTTONGAPSIZE, self.BUTTONSIZE, self.BUTTONSIZE)
        self.GREENRECT  = pg.Rect(self.XMARGIN + self.BUTTONSIZE + self.BUTTONGAPSIZE, self.YMARGIN + self.BUTTONSIZE + self.BUTTONGAPSIZE, self.BUTTONSIZE, self.BUTTONSIZE)
        
        # Set the font type and size
        self.BASICFONT = pg.font.Font('freesansbold.ttf', 45)
        
        # Button to close
        self.QUIT_SURF, self.QUIT_RECT = self.makeText('Close', WHITE, GREEN, self.WINDOWWIDTH - 200, self.WINDOWHEIGHT - 90)
        
        # load the sound files
        self.BEEP1 = pg.mixer.Sound(f'{CURRENT_DIR}/assets/sounds/beep1.ogg')
        self.BEEP2 = pg.mixer.Sound(f'{CURRENT_DIR}/assets/sounds/beep2.ogg')
        self.BEEP3 = pg.mixer.Sound(f'{CURRENT_DIR}/assets/sounds/beep3.ogg')
        self.BEEP4 = pg.mixer.Sound(f'{CURRENT_DIR}/assets/sounds/beep4.ogg')
    
    def play(self, playing: bool):
        # Initialize some variables for a new game
        pattern = self.CORRECT_SEQUENCE # PRESET PATTERN
        currentStep = 0 # the color the player must push next

        while playing: # main game loop
            clickedButton = None # button that was clicked (set to YELLOW, RED, GREEN, or BLUE)
            self.DISPLAYSURF.fill(self.bgColor)
            self.drawButtons()

            self.checkForQuit()
            for event in pg.event.get(): # event handling loop
                if event.type == pg.MOUSEBUTTONUP:
                    if self.QUIT_RECT.collidepoint(event.pos):
                        return
                    mousex, mousey = event.pos[0] - self.LOCATION[0], event.pos[1] - self.LOCATION[1]
                    clickedButton = self.getButtonClicked(mousex, mousey)
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        clickedButton = YELLOW
                    elif event.key == pg.K_w:
                        clickedButton = BLUE
                    elif event.key == pg.K_a:
                        clickedButton = RED
                    elif event.key == pg.K_s:
                        clickedButton = GREEN

            # wait for the player to enter buttons
            if clickedButton and clickedButton == pattern[currentStep]:
                # pushed the correct button
                self.flashButtonAnimation(clickedButton)
                currentStep += 1

                if currentStep == len(pattern): # Wins
                    self.flashButtonAnimation(clickedButton)
                    self.flashBackground(GREEN, 4, 4)
                    currentStep = 0
                    return False

            elif clickedButton and clickedButton != pattern[currentStep]: # Lose
                self.flashButtonAnimation(clickedButton)
                self.flashBackground(RED, 5)
                currentStep = 0

            self.update()
            
    def flashButtonAnimation(self, color, animationSpeed=50):
        if color == YELLOW:
            sound = self.BEEP1
            flashColor = BRIGHTYELLOW
            rectangle = self.YELLOWRECT
        elif color == BLUE:
            sound = self.BEEP2
            flashColor = BRIGHTBLUE
            rectangle = self.BLUERECT
        elif color == RED:
            sound = self.BEEP3
            flashColor = BRIGHTRED
            rectangle = self.REDRECT
        elif color == GREEN:
            sound = self.BEEP4
            flashColor = BRIGHTGREEN
            rectangle = self.GREENRECT

        origSurf = self.DISPLAYSURF.copy()
        flashSurf = pg.Surface((self.BUTTONSIZE, self.BUTTONSIZE))
        flashSurf = flashSurf.convert_alpha()
        r, g, b = flashColor
        sound.play()
        for start, end, step in ((0, 255, 1), (255, 0, -1)): # animation loop
            for alpha in range(start, end, animationSpeed * step):
                self.checkForQuit()
                self.DISPLAYSURF.blit(origSurf, (0, 0))
                flashSurf.fill((r, g, b, alpha))
                self.DISPLAYSURF.blit(flashSurf, rectangle.topleft)
                self.update()
        self.DISPLAYSURF.blit(origSurf, (0, 0))

    def drawButtons(self):
        pg.draw.rect(self.DISPLAYSURF, YELLOW, self.YELLOWRECT)
        pg.draw.rect(self.DISPLAYSURF, BLUE,   self.BLUERECT)
        pg.draw.rect(self.DISPLAYSURF, RED,    self.REDRECT)
        pg.draw.rect(self.DISPLAYSURF, GREEN,  self.GREENRECT)

    def getButtonClicked(self,x, y):
        if self.YELLOWRECT.collidepoint( (x, y) ):
            return YELLOW
        elif self.BLUERECT.collidepoint( (x, y) ):
            return BLUE
        elif self.REDRECT.collidepoint( (x, y) ):
            return RED
        elif self.GREENRECT.collidepoint( (x, y) ):
            return GREEN
        return None

    def flashBackground(self, color, times: int, number_repeats: int=1, delay: int=1, animationSpeed=20): 
        newBgColor = color
        
        newBgSurf = pg.Surface((self.WINDOWWIDTH, self.WINDOWHEIGHT))
        newBgSurf = newBgSurf.convert_alpha()   
        r, g, b = newBgColor
        
        for i in range(number_repeats):
            for i in range(times): # Flash "times" times
                for alpha in range(0, 255, animationSpeed): # animation loop
                    self.checkForQuit()
                    self.DISPLAYSURF.fill(self.bgColor)
                    newBgSurf.fill((r, g, b, alpha))
                    self.DISPLAYSURF.blit(newBgSurf, (0, 0))
                    self.drawButtons() # redraw the buttons on top of the tint
                    self.update()
            self.checkForQuit()
            
            # Effectively reset the board's color
            newBgSurf.fill(self.bgColor) 
            self.DISPLAYSURF.blit(newBgSurf, (0, 0))
            self.drawButtons() # redraw the buttons
            
            self.update()
            time.sleep(delay) # Sleep for 1 second and then flash again

                
class MemoryGame(Game):
    def __init__(self, image: pg.image, board_dimensions: tuple[int], dest_surf: pg.Surface, location: tuple[int], size: tuple[int], fps: int=60):
        super().__init__(dest_surf, location, size, fps)
        # Theme presets
        self.IMAGE = pg.transform.scale(image, (size[0], size[1]))
        self.BGCOLOR = GRAY
        self.LIGHTBGCOLOR = LIGHTGREY
        self.BOXCOLOR = WHITE
        self.HIGHLIGHTCOLOR = BLUE
        
        self.BASICFONT = pg.font.Font('freesansbold.ttf', 45)
        
        self.WINDOWWIDTH = size[0]
        self.WINDOWHEIGHT = size[1]
        self.REVEALSPEED = 3
        self.BOXSIZE = int(size[0] / 7)
        self.GAPSIZE = size[1] / 72
        self.BOARDWIDTH = board_dimensions[0]
        self.BOARDHEIGHT = board_dimensions[1]

        # Does the board have an even number of boxes?
        assert (self.BOARDWIDTH * self.BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
        self.XMARGIN = int((self.WINDOWWIDTH - (self.BOARDWIDTH * (self.BOXSIZE + self.GAPSIZE))) / 2)
        self.YMARGIN = int((self.WINDOWHEIGHT - (self.BOARDHEIGHT * (self.BOXSIZE + self.GAPSIZE))) / 2)
        
        # Shape presets
        self.DONUT = 'donut'
        self.SQUARE = 'square'
        self.DIAMOND = 'diamond'
        self.LINES = 'lines'
        self.OVAL = 'oval'
        
        # Back button
        self.QUIT_SURF, self.QUIT_RECT = self.makeText('Close', WHITE, GREEN, self.WINDOWWIDTH - 200, self.WINDOWHEIGHT - 90)
        
        # Do we have enough colors?
        self.ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
        self.ALLSHAPES = (self.DONUT, self.SQUARE, self.DIAMOND, self.LINES, self.OVAL)
        assert len(self.ALLCOLORS) * len(self.ALLSHAPES) * 2 >= self.BOARDWIDTH * self.BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."
        
        self.start_anim_played = False
        self.mainBoard = self.getRandomizedBoard()
        self.revealedBoxes = self.generateRevealedBoxesData(False)

    def play(self, playing: bool):
        # Mouse coordinates
        mousex = 0
        mousey = 0

        # These vars are 2d lists of board positions (where things are and what's covered)
        self.generateRevealedBoxesData(False)

        # Store coordinates of first box clicked
        firstSelection = None

        self.DISPLAYSURF.fill(self.BGCOLOR)
        self.DISPLAYSURF.blit(self.QUIT_SURF, self.QUIT_RECT)
        if not self.start_anim_played: # Only play the animation once
            self.startGameAnimation(self.mainBoard) # Gives you a sneak peak of the boxes
        self.start_anim_played = True

        # GAME loop 
        while playing:
            # Reset mouseClicked state
            mouseClicked = False

            # Draw the window (with revealedBoxes)
            self.DISPLAYSURF.fill(self.BGCOLOR)
            self.drawBoard(self.mainBoard, self.revealedBoxes)

            # EVENT loop
            for event in pg.event.get():
                # Could use a match case statement here
                # Escape key or window closed
                if event.type == pg.QUIT or (event.type == pg.KEYUP and event.key == pg.K_ESCAPE):
                    self.terminate()
                # Mouse moved
                elif event.type == pg.MOUSEMOTION:
                    mousex, mousey = event.pos[0] - self.LOCATION[0], event.pos[1] - self.LOCATION[1]
                # Mouse clicked
                elif event.type == pg.MOUSEBUTTONUP:
                    if self.QUIT_RECT.collidepoint(event.pos[0] - self.LOCATION[0], event.pos[1] - self.LOCATION[1]):
                        return
                    mousex, mousey = event.pos[0] - self.LOCATION[0], event.pos[1] - self.LOCATION[1]
                    mouseClicked = True
                    
            # Returns tuple of box coordinates
            boxx, boxy = self.getBoxAtPixel(mousex, mousey)
            if boxx != None and boxy != None:
                # The mouse is currently over a box.
                if not self.revealedBoxes[boxx][boxy]: # If box is not revealed
                    self.drawHighlightBox(boxx, boxy) # Highlight the box
                if not self.revealedBoxes[boxx][boxy] and mouseClicked: # If you click on a concealed box
                    self.revealBoxesAnimation(self.mainBoard, [(boxx, boxy)]) # Reveal box
                    self.revealedBoxes[boxx][boxy] = True # set the box as "revealed"
                    if firstSelection == None: # the current box was the first box clicked
                        firstSelection = (boxx, boxy)
                    else: # the current box was the second box clicked
                        # Check if there is a match between the two icons.
                        icon1shape, icon1color = self.getShapeAndColor(self.mainBoard, firstSelection[0], firstSelection[1])
                        icon2shape, icon2color = self.getShapeAndColor(self.mainBoard, boxx, boxy)

                        if icon1shape != icon2shape or icon1color != icon2color:
                            # Icons don't match. Re-cover up both selections.
                            pg.time.wait(1000) # 1000 milliseconds = 1 sec
                            self.coverBoxesAnimation(self.mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                            self.revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                            self.revealedBoxes[boxx][boxy] = False
                        elif self.hasWon(self.revealedBoxes): # check if all pairs found WIN STATE
                            self.DISPLAYSURF.blit(self.IMAGE, (0, 0))
                            self.update()
                            time.sleep(3)
                            return False
                        firstSelection = None # reset firstSelection variable

            # Redraw the screen and wait a clock tick.
            self.update()

    # Determine boxes revealed 
    def generateRevealedBoxesData(self, val):
        revealedBoxes = []
        for i in range(self.BOARDWIDTH):
            revealedBoxes.append([val] * self.BOARDHEIGHT)
        return revealedBoxes


    def getRandomizedBoard(self):
        # Get a list of every possible shape in every possible color.
        icons = []
        for color in self.ALLCOLORS:
            for shape in self.ALLSHAPES:
                icons.append( (shape, color) )

        # Randomize list
        random.shuffle(icons)
        numIconsUsed = int(self.BOARDWIDTH * self.BOARDHEIGHT / 2) # calculate how many icons are needed
        icons = icons[:numIconsUsed] * 2 # make two of each
        random.shuffle(icons)

        # Create the board data structure, with randomly placed icons.
        board = []
        for x in range(self.BOARDWIDTH):
            column = []
            for y in range(self.BOARDHEIGHT):
                column.append(icons[0])
                del icons[0] # remove the icons as we assign them
            board.append(column)
        return board

    # Split list into a list of lists of groupSize
    def splitIntoGroupsOf(self, groupSize, theList):
        # splits a list into a list of lists, where the inner lists have at
        # most groupSize number of items.
        result = []
        # three-param range?
        for i in range(0, len(theList), groupSize):
            result.append(theList[i:i + groupSize])
        return result

    # Box coords into pixel coords
    def leftTopCoordsOfBox(self, boxx, boxy):
        # Convert board coordinates to pixel coordinates
        left = boxx * (self.BOXSIZE + self.GAPSIZE) + self.XMARGIN
        top = boxy * (self.BOXSIZE + self.GAPSIZE) + self.YMARGIN
        return (left, top)

    # Pixel coords into box coords
    def getBoxAtPixel(self, x, y):
        for boxx in range(self.BOARDWIDTH):
            for boxy in range(self.BOARDHEIGHT):
                left, top = self.leftTopCoordsOfBox(boxx, boxy)
                boxRect = pg.Rect(left, top, self.BOXSIZE, self.BOXSIZE)
                if boxRect.collidepoint(x, y):
                    return (boxx, boxy)
        return (None, None)

    # Creating/drawing icons
    def drawIcon(self, shape, color, boxx, boxy):
        quarter = int(self.BOXSIZE * 0.25) # syntactic sugar
        half =    int(self.BOXSIZE * 0.5)  # syntactic sugar

        left, top = self.leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords
        # Draw the shapes, you could use a match case statement here
        if shape == self.DONUT:
            pg.draw.circle(self.DISPLAYSURF, color, (left + half, top + half), half - 5)
            pg.draw.circle(self.DISPLAYSURF, self.BGCOLOR, (left + half, top + half), quarter - 5)
        elif shape == self.SQUARE:
            pg.draw.rect(self.DISPLAYSURF, color, (left + quarter, top + quarter, self.BOXSIZE - half, self.BOXSIZE - half))
        elif shape == self.DIAMOND:
            pg.draw.polygon(self.DISPLAYSURF, color, ((left + half, top), (left + self.BOXSIZE - 1, top + half), (left + half, top + self.BOXSIZE - 1), (left, top + half)))
        elif shape == self.LINES:
            for i in range(0, self.BOXSIZE, 4):
                pg.draw.line(self.DISPLAYSURF, color, (left, top + i), (left + i, top))
                pg.draw.line(self.DISPLAYSURF, color, (left + i, top + self.BOXSIZE - 1), (left + self.BOXSIZE - 1, top + i))
        elif shape == self.OVAL:
            pg.draw.ellipse(self.DISPLAYSURF, color, (left, top + quarter, self.BOXSIZE, half))

    # Simple function to return tuple of shape and color values of a box
    def getShapeAndColor(self, board, boxx, boxy):
        # shape value for x, y spot is stored in board[x][y][0]
        # color value for x, y spot is stored in board[x][y][1]
        return board[boxx][boxy][0], board[boxx][boxy][1]

    # Covering the boxes
    def drawBoxCovers(self, board, boxes, coverage):
        # Draws boxes being covered/revealed. "boxes" is a list
        # of two-item lists, which have the x & y spot of the box.
        for box in boxes:
            left, top = self.leftTopCoordsOfBox(box[0], box[1])
            pg.draw.rect(self.DISPLAYSURF, self.BGCOLOR, (left, top, self.BOXSIZE, self.BOXSIZE))
            shape, color = self.getShapeAndColor(board, box[0], box[1])
            self.drawIcon(shape, color, box[0], box[1])
            if coverage > 0: # only draw the cover if there is an coverage
                pg.draw.rect(self.DISPLAYSURF, self.BOXCOLOR, (left, top, coverage, self.BOXSIZE))
        self.update()

    # Revealing a box
    def revealBoxesAnimation(self, board, boxesToReveal):
        # Do the "box reveal" animation.
        for coverage in range(self.BOXSIZE, (-self.REVEALSPEED) - 1, -self.REVEALSPEED):
            self.drawBoxCovers(board, boxesToReveal, coverage)

    # Covering a box (opposite of revealBoxesAnimation, and is very similar)
    def coverBoxesAnimation(self, board, boxesToCover):
        # Do the "box cover" animation.
        for coverage in range(0, self.BOXSIZE + self.REVEALSPEED, self.REVEALSPEED):
            self.drawBoxCovers(board, boxesToCover, coverage)

    # Draw each box
    def drawBoard(self, board, revealed: list[list]):
        self.DISPLAYSURF.blit(self.QUIT_SURF, self.QUIT_RECT)
        # Draws all of the boxes in their covered or revealed state.
        for boxx in range(self.BOARDWIDTH):
            for boxy in range(self.BOARDHEIGHT):
                left, top = self.leftTopCoordsOfBox(boxx, boxy)
                if not revealed[boxx][boxy]:
                    # Draw a covered box.
                    pg.draw.rect(self.DISPLAYSURF, self.BOXCOLOR, (left, top, self.BOXSIZE, self.BOXSIZE))
                else:
                    # Draw the (revealed) icon.
                    shape, color = self.getShapeAndColor(board, boxx, boxy)
                    self.drawIcon(shape, color, boxx, boxy)

    # Draw a blue outline around the box (show the user that they can click it)
    def drawHighlightBox(self, boxx, boxy):
        left, top = self.leftTopCoordsOfBox(boxx, boxy)
        pg.draw.rect(self.DISPLAYSURF, self.HIGHLIGHTCOLOR, (left - 5, top - 5, self.BOXSIZE + 10, self.BOXSIZE + 10), 4)
        
    # Reveal and cover groups of boxes (give user a hint)
    def startGameAnimation(self, board):
        # Randomly reveal the boxes 8 at a time.
        coveredBoxes = self.generateRevealedBoxesData(False)
        boxes = []
        for x in range(self.BOARDWIDTH):
            for y in range(self.BOARDHEIGHT):
                boxes.append( (x, y) )
        random.shuffle(boxes)
        boxGroups = self.splitIntoGroupsOf(8, boxes)

        self.drawBoard(board, coveredBoxes)
        for boxGroup in boxGroups:
            self.revealBoxesAnimation(board, boxGroup)
            self.coverBoxesAnimation(board, boxGroup)

    # Determine if the player has won if all boxes have been revealed
    def hasWon(self, revealedBoxes):
        # Returns True if all the boxes have been revealed, otherwise False
        for i in revealedBoxes:
            if False in i:
                return False # return False if any boxes are covered.
        return True
