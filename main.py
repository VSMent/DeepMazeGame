"""
Script for main game logic
"""

# imports, init

# globals()["pygame"] = __import__("pygame")
# globals()["time"] = __import__("time")
# globals()["math"] = __import__("math")
# globals()["atexit"] = __import__("atexit")
import pygame
import time
import math
import random
import gameVariables as g
from maze import Maze

# initialize all graphic related variables, pygame stuff
g.init()

# version check
try:
    # Python 2
    xrange
except NameError:
    # Python 3
    xrange = range

# variables

m = Maze()

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
lightGreen = (221, 255, 124)

# gameDisplay = pygame.display.set_mode((gameFullWidth,gameHeight),pygame.FULLSCREEN)
gameDisplay = pygame.display.set_mode((g.gameFullWidth, g.gameFullHeight))  # Initialize display
pygame.display.set_caption('Deep Maze!')  # Set title
clock = pygame.time.Clock()  # Initialize clock for changing game objects with time

playerWidth = int(round(g.blockSize / 1.29 / 1.3))  # relative player width (1.29 - original, cropped image ratio)
playerHeight = int(round(g.blockSize / 1.3))  # relative player height
playerImg = pygame.transform.scale(
    pygame.image.load("sprites/main-pack/hero/idleA/hero_idleA_0000.png").subsurface(20, 21, 62, 80),
    (playerWidth, playerHeight))  # crop, scale and load image
# chestImg = pygame.transform.scale(pygame.image.load("sprites/treasure chest/chest1_128.png"),
#                                   (int(g.blockSize * .8), int(g.blockSize * .8)))  # w:100 h:110
floorBlockImg = pygame.transform.scale(
    pygame.image.load("sprites/main-pack/level/groundEarth_checkered_7x10.png"),
    (int(g.blockSize), int(g.blockSize * 2)))  # load floor block image
wallBlockImg = pygame.transform.scale(
    pygame.image.load("sprites/main-pack/level/wallBreakable_7x5+.png"),
    (int(g.blockSize * 1), int(g.blockSize * 1.5)))  # load wall image
exitBlockImg = pygame.transform.scale(
    pygame.image.load("sprites/main-pack/level/groundExitDown_7x5.png"),
    (int(g.blockSize * 1), int(g.blockSize * 1)))  # load exit image


# code
def draw_image(image, row, col, centered=False):
    """
    Used to draw any image
    :param image: pygame image
    :param row: int, number of row (y position)
    :param col: int, number of column (x position)
    :param centered: boolean, add offsets if image is smaller than blockSize
    """
    # Wall (50% offset down)
    if image == wallBlockImg:
        row += (math.ceil(float(wallBlockImg.get_height()) / float(g.blockSize)) - (
                float(wallBlockImg.get_height()) / float(g.blockSize)))

    if not centered:
        gameDisplay.blit(image, (col * g.blockSize + g.offsetH1, row * g.blockSize + g.offsetV1))  # just draw
    else:
        localOffsetX = abs((g.blockSize - image.get_width()) / 2)
        localOffsetY = abs((g.blockSize - image.get_height()) / 2)
        gameDisplay.blit(image, (col * g.blockSize + localOffsetX + g.offsetH1, row * g.blockSize + localOffsetY + g.offsetV1))  #draw with offsets


def draw_grid():
    """
    Show grid, for debug only
    """
    for col in xrange(1, g.cols):
        pygame.draw.line(gameDisplay, red, (col * g.blockSize + g.offsetH1, g.offsetV1),
                         (col * g.blockSize + g.offsetH1, g.gameHeight), 1)  # draw column lines
    for row in xrange(1, g.gridRows):
        pygame.draw.line(gameDisplay, red, (g.offsetH1, row * g.blockSize + g.offsetV1), (
            g.gameWidth, row * g.blockSize + g.offsetV1), 1)  # draw row lines


def draw_floor():
    """
    Separate function to draw floor (background layer)
    TODO: merge into draw_maze function
    """
    for row in xrange(1, g.rows + 1):
        for col in xrange(0, g.cols):
            draw_image(floorBlockImg, row, col)


def draw_maze(level, playerRow, playerCol):
    """
    Draw any level of the maze
    :param level: int, number of level
    :param playerRow: int, number of row (y position) with current player position
    :param playerCol: int, number of column (x position) with current player position
    """
    draw_floor()  # show grass bg
    for row in xrange(g.rows):
        for col in xrange(g.cols):
            # FG wall
            if get_nth_digit(level[row][col], m.patternFgDigit) == m.patternFgWall:  # wall on fg layer
                draw_image(wallBlockImg, row, col)
            # MG exit
            if get_nth_digit(level[row][col], m.patternMgDigit) == m.patternMgExit:  # exit on mg layer
                draw_image(exitBlockImg, row + 1, col, True)
            # FG player
            if get_nth_digit(level[row][col], m.patternFgDigit) == m.patternFgPlayer:  # player on fg layer
                draw_image(playerImg, playerRow + 1, playerCol, True)
    check_exit(level, playerRow, playerCol)  # after all was drawn check if player has is at exit


def check_exit(level, playerRow, playerCol):
    """
    Move to next level if this one is complete
    :param level: int, current level
    :param playerRow: int, number of row (y position) with current player position
    :param playerCol: int, number of column (x position) with current player position
    """
    if get_nth_digit(level[playerRow][playerCol], m.patternMgDigit) == m.patternMgExit:  # exit on mg layer
        display_message("Level complete!")  # draw text
        m.currentLevel += 1  # increase level counter
        game_loop()  # start game loop again


def get_nth_digit(number, n):
    """
    Show n-th digit of number
    :param number: int, original number
    :param n: int, digit position, right is 0, increasing to the left
    :return: int, n-th digit
    """
    return number // 10 ** n % 10


def move_player(keys, playerRow, playerCol):
    """
    Change player position in the level matrix
    :param keys: array, pygame pressed keys
    :param playerRow: int, number of row (y position) with current player position
    :param playerCol: int, number of column (x position) with current player position
    :return: tuple(
        canMove: boolean, allow or delay next move,
        playerRow: int, number of row (y position) with current player position
        playerCol: int, number of column (x position) with current player position)
    TODO: move repetitive operations to separate function (m.levels... -= / += m.patternFgPlayer...)
    """
    # X axis
    if keys[pygame.K_LEFT] and get_nth_digit(m.levels[m.currentLevel][playerRow][playerCol - 1],
                                             m.patternMgDigit) in m.walkableMgObjects:
        m.levels[m.currentLevel][playerRow][playerCol] -= m.patternFgPlayer * 10 ** m.patternFgDigit  # erase player
        playerCol -= 1
        m.levels[m.currentLevel][playerRow][playerCol] += m.patternFgPlayer * 10 ** m.patternFgDigit  # add player
        m.print_maze_level(m.currentLevel)  # debug print maze matrix
        return  playerRow, playerCol  # delay movement, return new player coordinates
    if keys[pygame.K_RIGHT] and get_nth_digit(m.levels[m.currentLevel][playerRow][playerCol + 1],
                                              m.patternMgDigit) in m.walkableMgObjects:
        m.levels[m.currentLevel][playerRow][playerCol] -= m.patternFgPlayer * 10 ** m.patternFgDigit
        playerCol += 1
        m.levels[m.currentLevel][playerRow][playerCol] += m.patternFgPlayer * 10 ** m.patternFgDigit
        m.print_maze_level(m.currentLevel)
        return  playerRow, playerCol

    # Y axis
    if keys[pygame.K_UP] and get_nth_digit(m.levels[m.currentLevel][playerRow - 1][playerCol],
                                           m.patternMgDigit) in m.walkableMgObjects:
        m.levels[m.currentLevel][playerRow][playerCol] -= m.patternFgPlayer * 10 ** m.patternFgDigit
        playerRow -= 1
        m.levels[m.currentLevel][playerRow][playerCol] += m.patternFgPlayer * 10 ** m.patternFgDigit
        m.print_maze_level(m.currentLevel)
        return  playerRow, playerCol
    if keys[pygame.K_DOWN] and get_nth_digit(m.levels[m.currentLevel][playerRow + 1][playerCol],
                                             m.patternMgDigit) in m.walkableMgObjects:
        m.levels[m.currentLevel][playerRow][playerCol] -= m.patternFgPlayer * 10 ** m.patternFgDigit
        playerRow += 1
        m.levels[m.currentLevel][playerRow][playerCol] += m.patternFgPlayer * 10 ** m.patternFgDigit
        m.print_maze_level(m.currentLevel)
        return  playerRow, playerCol

    return  playerRow, playerCol  # allow movement, return current player coordinates


def text_objects(text, font):
    """
    Prepare text for displaying
    :param text: string, text to show
    :param font: pygame font, font to draw text
    :return: tuple(
        pygame surface, surface with the text drawn on
        pygame rect, surface wireframe to move around)
    """
    textSurface = font.render(text, True, black)  # create text image surface
    return textSurface, textSurface.get_rect()


def display_message(text):
    """
    Show message on the center of play area
    :param text: string, any text to show
    """
    largeText = pygame.font.Font('freesansbold.ttf', 115)  # define font, size
    TextSurf, TextRect = text_objects(text, largeText)  # get image, wireframe
    TextRect.center = ((g.gameWidth / 2), (g.gameHeight / 2))  # change wirefrawme position
    gameDisplay.blit(TextSurf, TextRect)  # show image on wireframe
    pygame.display.update()  # notify pygame there was an update
    time.sleep(2)  # wait for 2 seconds


def game_loop():
    """
    Main loop of the game
    """
    m.generate_maze(g.rows, g.cols)  # generate maze
    m.print_maze_level(m.currentLevel)  # debug show result
    # variables
    # draw_maze(m.levels[m.currentLevel])
    playerRow = m.initialPlayerPos[0]  # set alias for player row
    playerCol = m.initialPlayerPos[1]  # set alias for player col
    gameExit = False  # not in use, cycle interrupt wariable
    # canMove = False  # forbid player to move
    # main loop
    while not gameExit:
        for event in pygame.event.get():  # get all pygame events
            # print(event) # DEBUG
            if event.type == pygame.QUIT:
                quit()  # exit from application

            keys = pygame.key.get_pressed()  # array of all pressed keys
            # move player
            if event.type == g.MOVEEVENT:  # if move event happen
                playerRow, playerCol = move_player(keys, playerRow, playerCol)  # move player

        gameDisplay.fill(lightGreen)  # draw background color
        # draw sidebar (black rectangle for now)
        pygame.draw.rect(gameDisplay, black,
                         pygame.Rect(g.gameWidth + g.offsetH1 + g.offsetH2, 0, g.sidebarWidth, g.gameFullHeight), 0)
        draw_maze(m.levels[m.currentLevel], playerRow, playerCol)  # draw maze level
        # draw_grid()  # debug
        pygame.display.update()  # update specific thing if specified or whole screen
        clock.tick(60)  # run on 60 fps

game_loop()  # start game loop
# quit
quit()
