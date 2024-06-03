import os
import random, sys, time, pygame
from pygame.locals import *

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FLASHSPEED = 500
FLASHDELAY = 200
BUTTONSIZE = 200
BUTTONGAPSIZE = 20
TIMEOUT = 4 # seconds before game over if no button is pushed

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BRIGHTRED = (255, 0, 0)
RED = (155, 0, 0)
BRIGHTGREEN = (0, 255, 0)
GREEN = (0, 155, 0)
BRIGHTBLUE = (0, 0, 255)
BLUE = (0, 0, 155)
BRIGHTYELLOW = (255, 255, 0)
YELLOW = (155, 155, 0)
DARKGRAY = (40, 40, 40)
bgColor = BLACK

XMARGIN = int((WINDOWWIDTH - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)

YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
REDRECT = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
GREENRECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
# the four above variables are the buttons being clicked or pressed for the pattern

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Simulate')
    # sets title of program in the window display

    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)

    infoSurf = BASICFONT.render('Match the pattern by clicking on the button using the Q, W, A, S keys.', 1, DARKGRAY)
    # game info instructions
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOWHEIGHT - 25)
    # load the sound files
    BEEP1 = pygame.mixer.Sound('beep1.ogg')
    BEEP2 = pygame.mixer.Sound('beep2.ogg')
    BEEP3 = pygame.mixer.Sound('beep3.ogg')
    BEEP4 = pygame.mixer.Sound('beep4.ogg')

    # initialize some variables for the new game
    pattern = [] # stores the pattern of colors the player must memorize on each turn
    currentStep = 0 # the color the player must push next in each pattern
    lastClickTime = 0 # time stamp of the players last button push. this works in conjunction with the TIMEOUT const to moniter
    # the time between button clicks. 
    score = 0
    # when false, the pattern is playing. when True, Waiting foe the player to click a colored button
    waitingForInput = False

    while True:
        clickedButton = None # Botton the was clicked (set to YELLOW, RED, GREEN or BLUE). resets to none at the begining of each iteration
        DISPLAYSURF.fill(bgColor)
        drawButtons()

        scoreSurf = BASICFONT.render('Score: ' + str(score), 1, WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 100, 10)
        DISPLAYSURF.blit(scoreSurf, scoreRect)

        DISPLAYSURF.blit(infoSurf, infoRect)

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex, mousey)
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    clickedButton = YELLOW
                elif event.key == K_w:
                    clickedButton = BLUE
                elif event.key == K_a:
                    clickedButton = RED
                elif event.key == K_s:
                    clickedButton = GREEN
                # lets user input with either mouse clicks or button presses

            if not waitingForInput: # play the pattern
                pygame.display.update()
                pygame.time.wait(1000)
                pattern.append(random.choice((YELLOW, BLUE, RED, GREEN)))
                # ^ adds random choice to make the pattern one step longer
                for button in pattern:
                    flashButtonAnimation(button)
                    pygame.time.wait(FLASHDELAY)
                    # plays flashbutton animation for each button in the pattern
                waitingForInput = True
            else:
                # wait for the player to enter buttons
                if clickedButton and clickedButton == pattern[currentStep]:
                    # if check to see if player pushed the correct button
                    flashButtonAnimation(clickedButton)
                    currentStep += 1
                    lastClickTime = time.time()

                    if currentStep == len(pattern): # checks if last button pushed was correct by checking if int stored incurrentstep is == to pattern length
                        # pushed the last button in the pattern
                        changeBackgroundAnimation()
                        score += 1
                        waitingForInput = False
                        currentStep = 0 # reset back to first step
                # 109 - 120 are inside of the else statment on 107 so that the programs knows that the player
                #clicked on the last button in the pattern and that it was the correct one

                elif (clickedButton and clickedButton != pattern[currentStep]) or (currentStep != 0 and time.time() - TIMEOUT > lastClickTime):
                    # player has pushed the incorrect button, of has timed out
                    # also checks if player is in the midst of clicking with 'currentStep != 0' and the time between timeout and last btn click
                    gameOverAnimation()
                    # reset the variables for the new game:
                    pattern = []
                    currentStep = 0
                    waitingForInput = False
                    score = 0
                    pygame.time.wait(1000)
                    changeBackgroundAnimation()

            pygame.display.update()
            FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the quit events
        terminate() # terminate if any quit events are present
    for event in pygame.event.get(KEYUP): # get all the key up events
        if event.key == K_ESCAPE:
            terminate() # terminate if the keyup event was for the escape key
        pygame.event.post(event) # put the othe KEYUP event objects back

def flashButtonAnimation(color, animationSpeed=50):
    if color == YELLOW:
        sound = BEEP1
        flashColor = BRIGHTYELLOW
        rectangle = YELLOWRECT
    elif color == BLUE:
        sound = BEEP2
        flashColor = BRIGHTBLUE
        rectangle = BLUERECT
    elif color == RED:
        sound = BEEP3
        flashColor = BRIGHTRED
        rectangle = REDRECT
    elif color == GREEN:
        sound = BEEP4
        flashColor = BRIGHTGREEN
        rectangle = GREENRECT
    # ^ these flash the brightened version of the box's color when clicked

    origSurf = DISPLAYSURF.copy() # draws a copy of the display surface 
    flashSurf = pygame.Surface((BUTTONSIZE, BUTTONSIZE)) # draws the flashing color btn over original btn
    flashSurf = flashSurf.convert_alpha() # alpha starts at 0 the slowly comes to full opacity, gives illusion of brigthening
    r, g, b = flashColor
    sound.play() # plays sound during btn animation
    for start, end, step in ((0, 255, 1), (255, 0, -1)): # animation loop
        # ^ brightens then dims. brighten ex: start is 0, end is 255, step is 1
        for alpha in range(start, end, animationSpeed * step):
            checkForQuit()
            DISPLAYSURF.blit(origSurf, (0, 0))
            flashSurf.fill((r, g, b, alpha)) # fills surface with r, g, b values and alpha value
            DISPLAYSURF.blit(flashSurf, rectangle.topleft)
            pygame.display.update() # ensures computer does not play the animation as fast as possible
            FPSCLOCK.tick(FPS) # play speed of animations
            DISPLAYSURF.blit(origSurf, (0, 0))

def drawButtons():
    pygame.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECT)
    pygame.draw.rect(DISPLAYSURF, BLUE, BLUERECT)
    pygame.draw.rect(DISPLAYSURF, RED, REDRECT)
    pygame.draw.rect(DISPLAYSURF, GREEN, GREENRECT)

def changeBackgroundAnimation(animationSpeed=40):
    global bgColor
    newBgColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    newBgSurf = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
    newBgSurf = newBgSurf.convert_alpha()
    r, g, b = newBgColor
    for alpha in range(0, 255, animationSpeed): # animation loop
        checkForQuit()
        DISPLAYSURF.fill(bgColor) # fiils display with bgcolor

        newBgSurf.fill((r, g, b, alpha))
        DISPLAYSURF.blit(newBgSurf, (0, 0)) # new fill for bg

        drawButtons() # redraw the buttons ontop of the tint

        pygame.display.update() # draws display surface on screen and adds pause
        FPSCLOCK.tick(FPS)
    bgColor = newBgColor

def gameOverAnimation(color=WHITE, animationSpeed=50):
    # play all the beeps at once then flash the background
    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface(DISPLAYSURF.get_size())
    flashSurf = flashSurf.convert_alpha()
    BEEP1.play() # play all four beeps at the same time... sorta
    BEEP2.play()
    BEEP3.play()
    BEEP4.play()
    r, g, b = color
    for i in range(3): # do the flash 3 times
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(start, end, animationSpeed * step):
                checkForQuit()
                flashSurf.fill((r, g, b, alpha))
                DISPLAYSURF.blit(origSurf, (0, 0))
                DISPLAYSURF.blit(flashSurf, (0, 0))
                drawButtons()
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def getButtonClicked(x, y):
    # gets the x and y coordinates for the buttons if clicked and returns 'none' if none of them are clicked
    if YELLOWRECT.collidepoint( (x, y) ):
        return YELLOW
    elif BLUERECT.collidepoint( (x, y) ):
        return BLUE
    elif REDRECT.collidepoint( (x, y) ):
        return RED
    elif GREENRECT.collidepoint( (x, y) ):
        return GREEN
    return None


if __name__ == '__main__':
    main()



