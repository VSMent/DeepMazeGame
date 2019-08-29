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

playerSpeed = g.gameWidth / 180  # how much pixels should player move

m = Maze()

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
lightGreen = (221, 255, 124)

# gameDisplay = pygame.display.set_mode((gameFullWidth,gameHeight),pygame.FULLSCREEN)
gameDisplay = pygame.display.set_mode((g.gameFullWidth, g.gameFullHeight))
pygame.display.set_caption('Deep Maze!')
clock = pygame.time.Clock()

playerWidth = int(round(g.blockSize / 1.29 / 1.3))
playerHeight = int(round(g.blockSize / 1.3))
playerImg = pygame.transform.scale(
    pygame.image.load("sprites/main-pack/hero/idleA/hero_idleA_0000.png").subsurface(20, 21, 62, 80),
    (playerWidth, playerHeight))
chestImg = pygame.transform.scale(pygame.image.load("sprites/treasure chest/chest1_128.png"),
                                  (int(g.blockSize * .8), int(g.blockSize * .8)))  # w:100 h:110
# chestImg = pygame.transform.scale(pygame.image.load("sprites/wk/loot05key.png"),(int(g.blockSize*1),
# int(g.blockSize*1))) # w:100 h:110 floorBlockImg = pygame.image.load(
# "sprites/main-pack/level/groundEarth_checkered.png")
floorBlockImg = pygame.transform.scale(
    pygame.image.load("sprites/main-pack/level/groundEarth_checkered_7x10.png"),
    (int(g.blockSize), int(g.blockSize * 2)))
wallBlockImg = pygame.transform.scale(
    pygame.image.load("sprites/main-pack/level/wallBreakable_7x5+.png"),
    (int(g.blockSize * 1), int(g.blockSize * 1.5)))
exitBlockImg = pygame.transform.scale(
    pygame.image.load("sprites/main-pack/level/groundExitDown_7x5.png"),
    (int(g.blockSize * 1), int(g.blockSize * 1)))


# bgImg = pygame.transform.scale(
#     pygame.image.load("sprites/bg.jpg"),
#     (gameWidth, gameHeight))


# code
def drawImage(image, x, y, centered=False):
    # Wall
    if image == wallBlockImg:
        y += (math.ceil(float(wallBlockImg.get_height()) / float(g.blockSize)) - (
                float(wallBlockImg.get_height()) / float(g.blockSize))) * g.blockSize

    if not centered:
        gameDisplay.blit(image, (x + g.offsetH1, y + g.offsetV1))
    else:
        localOffsetX = abs((g.blockSize - image.get_width()) / 2)
        localOffsetY = abs((g.blockSize - image.get_height()) / 2)
        gameDisplay.blit(image, (x + localOffsetX + g.offsetH1, y + localOffsetY + g.offsetV1))


def drawGrid():
    for col in xrange(1, g.cols):
        pygame.draw.line(gameDisplay, red, (col * g.blockSize + g.offsetH1, g.offsetV1),
                         (col * g.blockSize + g.offsetH1, g.gameHeight), 1)
    for row in xrange(1, g.gridRows):
        pygame.draw.line(gameDisplay, red, (g.offsetH1, row * g.blockSize + g.offsetV1), (
            g.gameWidth, row * g.blockSize + g.offsetV1), 1)


def drawFloor(level):
    for row in xrange(1, g.rows + 1):
        for col in xrange(0, g.cols):
            # print(row,col)
            # if level[row][col] // 10 ** m.patternBgDigit % 10 == m.patternBgGrass:
            drawImage(floorBlockImg, col * g.blockSize, row * g.blockSize)


def drawMaze(level, playerRow, playerCol):
    drawFloor(level)
    for row in xrange(g.rows):
        for col in xrange(g.cols):
            # FG wall
            if getNthDigit(level[row][col], m.patternFgDigit) == m.patternFgWall:
                drawImage(wallBlockImg, col * g.blockSize, row * g.blockSize)
            # MG exit
            if getNthDigit(level[row][col], m.patternMgDigit) == m.patternMgExit:
                drawImage(exitBlockImg, col * g.blockSize, (row + 1) * g.blockSize, True)
            # FG player
            if getNthDigit(level[row][col], m.patternFgDigit) == m.patternFgPlayer:
                drawImage(playerImg, playerCol * g.blockSize, (playerRow + 1) * g.blockSize, True)
    if m.goToNextLevel:
        m.goToNextLevel = False
        m.currentLevel += 1
        displayMessage("Level Complete")
        gameLoop()


def getNthDigit(number, n):
    return number // 10 ** n % 10


def movePlayer(keys, playerRow, playerCol):
    def changeCoordinates(newRow, newCol):
        # global playerRow, playerCol
        print(playerRow,playerCol,newRow,newCol)
        m.levels[m.currentLevel][playerRow][playerCol] -= m.patternFgPlayer * 10 ** m.patternFgDigit
        m.levels[m.currentLevel][newRow][newCol] += m.patternFgPlayer * 10 ** m.patternFgDigit

    notMoved = True
    # X axis
    if keys[pygame.K_LEFT] and getNthDigit(m.levels[m.currentLevel][playerRow][playerCol - 1],
                                           m.patternMgDigit) in m.walkableFgObjects:
        # playerRow += -g.blockSize
        playerCol -= 1
        changeCoordinates(playerRow, playerCol)
        m.showMazeMap(m.currentLevel)
        # print("Row: "+str(playerRow),"Col: "+str(playerCol))
        notMoved = False
    if keys[pygame.K_RIGHT] and getNthDigit(m.levels[m.currentLevel][playerRow][playerCol + 1],
                                            m.patternMgDigit) in m.walkableFgObjects:
        playerCol += 1
        changeCoordinates(playerRow, playerCol)
        m.showMazeMap(m.currentLevel)
        # print("Row: "+str(playerRow),"Col: "+str(playerCol))
        notMoved = False

    # Y axis
    if keys[pygame.K_UP] and getNthDigit(m.levels[m.currentLevel][playerRow - 1][playerCol],
                                         m.patternMgDigit) in m.walkableFgObjects:
        playerRow -= 1
        changeCoordinates(playerRow, playerCol)
        m.showMazeMap(m.currentLevel)
        # print("Row: "+str(playerRow),"Col: "+str(playerCol))
        notMoved = False
    if keys[pygame.K_DOWN] and getNthDigit(m.levels[m.currentLevel][playerRow + 1][playerCol],
                                           m.patternMgDigit) in m.walkableFgObjects:
        playerRow += 1
        changeCoordinates(playerRow, playerCol)
        m.showMazeMap(m.currentLevel)
        # print("Row: "+str(playerRow),"Col: "+str(playerCol))
        notMoved = False

    # check if exit
    if getNthDigit(m.levels[m.currentLevel][playerRow][playerCol], m.patternMgDigit) == m.patternMgExit:
        m.goToNextLevel = True

    return notMoved, playerRow, playerCol


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def displayMessage(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((g.gameWidth / 2), (g.gameHeight / 2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)


def end():
    displayMessage('The end!')


def gameLoop():
    m.generateMaze(g.cols, g.rows, m.currentLevel)
    m.showMazeMap(m.currentLevel)
    # variables
    # drawMaze(m.levels[0])
    playerRow = m.initialPlayerPos[0]
    playerCol = m.initialPlayerPos[1]
    dx = 0
    dy = 0
    gameExit = False
    canMove = False
    # main loop
    while not gameExit:
        for event in pygame.event.get():
            # print(event) # DEBUG
            if event.type == pygame.QUIT:
                quit()

            keys = pygame.key.get_pressed()
            # move player
            if event.type == g.MOVEEVENT:
                canMove = True

            if canMove:
                canMove, playerRow, playerCol = movePlayer(keys, playerRow, playerCol)

    # gameDisplay.fill(white)
    # if playerRow < offsetH1 or playerRow > gameWidth - playerWidth:
    #   end()
    # if playerCol < offsetV1 or playerCol > gameHeight - playerHeight:
    #   end()
    gameDisplay.fill(lightGreen)
    # sidebar
    pygame.draw.rect(gameDisplay, black,
                     pygame.Rect(g.gameWidth + g.offsetH1 + g.offsetH2, 0, g.sidebarWidth, g.gameFullHeight), 0)
    drawMaze(m.levels[m.currentLevel], playerRow, playerCol)
    # drawGrid()
    # drawImage(wallBlockImg, 1 * g.blockSize, 4 * g.blockSize)
    # drawImage(wallBlockImg, 1 * g.blockSize, math.ceil(5 * g.blockSize))
    # drawImage(wallBlockImg, 2 * g.blockSize, math.ceil(4 * g.blockSize))
    # drawImage(wallBlockImg, 2 * g.blockSize, math.ceil(5 * g.blockSize))
    # drawImage(wallBlockImg, 2 * g.blockSize, math.ceil(6 * g.blockSize))
    # drawImage(wallBlockImg, 3 * g.blockSize, math.ceil(5 * g.blockSize))
    # drawImage(chestImg, 1 * g.blockSize, 1 * g.blockSize, True)
    pygame.display.update()  # update specific thing if specified or whole screen
    clock.tick(60)


gameLoop()
# quit
quit()
