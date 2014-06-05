# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license
# Modified by Elvyn Mejia

import random, pygame, sys
from pygame.locals import *

FPS = 15
WINDOWWIDTH = 960#the width of the window is 960 
WINDOWHEIGHT = 800#the height of the window is 800
CELLSIZE = 20#the size of every little square within the window

#inser debugging insertions 
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)#the width of each cell is WINDOWWIDTH/CELLSIZE
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)#the height of the cell each cell is WINDOWHEIGHT/CELLSIZE

#additive color model Red, Green, Blue
#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
AQUA      = (  0, 255, 255)#ADDED NEW COLORS BELOW 
BLUE      = (  0,   0, 255)
FUCHSIA   = (255,   0, 255)
GRAY      = (128, 128, 128)
LIME      = (  0, 255,   0)
MAROON    = (128,   0,   0)
NAVYBLUE  = (  0,   0, 128)
OLIVE     = (128, 128,   0)
PURPLE    = (128,   0, 128)
SILVER    = (192, 192, 192)
TEAL      = (  0, 128, 128)
YELLOW    = (255, 255,   0)
BGCOLOR = BLACK

#up, down, right and left directions
#keys to control the movement of the worm 
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

def main():#main function where everything is execuated
    
    #playWormySound = play_a_different_song()#randomly play a song while playing
    
    global FPSCLOCK, DISPLAYSURF, BASICFONT#global variables 

    pygame.init()#function call 
    FPSCLOCK = pygame.time.Clock()
    ## pass a tuple value of two integers W, and H, to draw a surface object
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) 
    BASICFONT = pygame.font.Font('freesansbold.ttf', 20)#20pt font type 
    pygame.display.set_caption('Welcome to the Wormy Game!')#display caption 

    showStartScreen()
    while True:
        runGame()#run game while condition is True
        showGameOverScreen()#while false game over


def runGame():#define a function called runGame
    playWormySound = play_a_different_song()#randomly play a song while playing
    # Set a random start point
    #start the worm in a random place moving right 
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    #worm coordinates
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    # Start the apple in a random place.
    apple = getRandomLocation()

    while True: # main game loop

        #1.Handles events.
        #2.Updates the game state.
        #3.Draws the game state to the screen.
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:#terminate loop if event.type==QUIT
                terminate()
                #different kind of events the object represents 
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return # if the worms has hit itself-game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return #  if the worms has hit the edges-game over

        # check if worm has eaten an apple
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation() # set a new apple somewhere
            playWormySound = wormySound()
        else:
            del wormCoords[-1] # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)#fill surface with BLACK color 
        drawGrid()#draw a grid
        drawWorm(wormCoords)#draw the worm given it coordinations 
        drawApple(apple)#draw apple 
        drawScore(len(wormCoords) - 3)
        pygame.display.update()#dislplays and update game events to the creeen 
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():#draws a message "Press key to play"
    pressKeySurf = BASICFONT.render('Press a key to play.', True, WHITE)#white color
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)#where to display 
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():#check for key events 
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():#draws the Wormy anf ymroW when the screen starts 
    titleFont = pygame.font.Font('freesansbold.ttf', 150)#original 100
    titleSurf1 = titleFont.render('!ymroW', True, WHITE)#frames to be rotated
    titleSurf2 = titleFont.render('Wormy!', True, RED)#frames to be rotated

    degrees1 = 0#degrees to which each frame rotate to and how fast
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BLACK)#fill in surface of StartScreen with BLACK color
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)#rotate frame to the left 
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)#centerframe1 
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)#rotate frame fo the right 
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)#Center frame2 
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 5 # rotate frame by 5 degrees to the left 
        degrees2 -= 5 # rotate frame by 5 drgrees to the right 


def terminate():
    pygame.quit()#quit pygame
    sys.exit()#exit system


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():#define a function to display Game Over 
    gameOverFont = pygame.font.Font('freesansbold.ttf', 200)
    gameSurf = gameOverFont.render('Game', True, RED)#display Game in RED
    overSurf = gameOverFont.render('Over', True, WHITE)#display Over in WHITE
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)#display message at midtop
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)#display message at midtop

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()#update game events 
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawScore(score):#function do draw and update score 
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, RED)#Display score in RED 
    scoreRect = scoreSurf.get_rect()
    scoreRect.topright = (WINDOWWIDTH - 860, 10)#where todisplay score
    DISPLAYSURF.blit(scoreSurf, scoreRect)#dislpay the score


def drawWorm(wormCoords):#function to draw the worm given its coordinates 
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE#draw the worm within a cell 
        y = coord['y'] * CELLSIZE#draw the worm within a cell
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, WHITE, wormSegmentRect)#WHITE outer segment 
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, DARKGRAY, wormInnerSegmentRect)#DARKGRAY inner segment 


def drawApple(coord):#draw the apple within a cell
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


def drawGrid():#function draws a grid of WINDOWWIDTH * WINDOWHEIGHT
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))
        
def play_a_different_song():
    #create a list of songs to play randomly when the game starts
    list_of_songs = ["M83 - Midnight City.mp3", "MGMT - Kids.mp3",
                     "The Offspring - The Kids Aren't Alright.mp3"]
    #add a flag to indicate which song is currently playing
    songCurrently_playing = None

    #initialize mixer module 
    pygame.mixer.init(frequency=22050, size= -16, channels=2, buffer=4096)
    global songCurrently_playing, list_of_songs
    next_song = random.choice(list_of_songs)#chose a random song from a list of songs 
    while next_song == songCurrently_playing:#play next a song while currently playing = None
        next_song = random.choice(list_of_songs)
    songCurrently_playing = next_song
    pygame.mixer.music.load(next_song)# load next random song 
    pygame.mixer.music.play()# play song
    pygame.mixer.music.queue(next_song)
    

def wormySound():
    #create a sound object. When the worm eats an apple, the sound object is called:)              
    #intialize mixer system
    pygame.mixer.init(frequency=22050, size= -16, channels=2, buffer=4096)

    #load music file
    effect = pygame.mixer.Sound("button-9.wav")

    #play music file 
    effect.play()

if __name__ == '__main__':#call main function to execuate function within main 
    main()
