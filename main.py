"""
Script for main game logic
"""

# imports, init
import pygame
import time
import math
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

playerSpeed = g.gameWidth / 180 # how much pixels should player move


m = Maze(g.cols, g.rows, g.blockSize)
m.generateMaze()

print('\n'.join([''.join(['{!s:5}'.format(item) for item in row])
                 for row in m.levels[0]]))


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
# chestImg = pygame.transform.scale(pygame.image.load("sprites/wk/loot05key.png"),(int(g.blockSize*1),int(g.blockSize*1))) # w:100 h:110
# floorBlockImg = pygame.image.load("sprites/main-pack/level/groundEarth_checkered.png")
floorBlockImg = pygame.transform.scale(
  pygame.image.load("sprites/main-pack/level/groundEarth_checkered_7x10.png"),
  (int(g.blockSize), int(g.blockSize*2)))
wallBlockImg = pygame.transform.scale(
  pygame.image.load("sprites/main-pack/level/wallBreakable_7x5+.png"),
  (int(g.blockSize*1), int(g.blockSize*1.5)))
# bgImg = pygame.transform.scale(
#     pygame.image.load("sprites/bg.jpg"),
#     (gameWidth, gameHeight))


# code
def showPlayer(x, y):
  drawImage(playerImg,x,y,True)

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
    pygame.draw.line(gameDisplay, red, (col * g.blockSize + g.offsetH1, g.offsetV1), (col * g.blockSize + g.offsetH1,
                                                                                      g.gameHeight), 1)
  for row in xrange(1, g.gridRows):
    pygame.draw.line(gameDisplay, red, (g.offsetH1, row * g.blockSize + g.offsetV1), (
      g.gameWidth, row * g.blockSize + g.offsetV1), 1)


def drawFloor():
  for col in xrange(0, g.cols):
    for row in xrange(1, g.rows + 1):
      gameDisplay.blit(floorBlockImg, (col * g.blockSize + g.offsetH1, row * g.blockSize + g.offsetV1))


def drawMaze(level):
  for i in range(g.rows):
    for j in range(g.cols):
      if level[i][j] == 1:
        drawImage(wallBlockImg, j * g.blockSize, i * g.blockSize)


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
  gameLoop()


def end():
  displayMessage('The end!')


def gameLoop():
  # variables
  # drawMaze(m.levels[0])
  playerX = (g.blockSize * 5 + g.offsetH1)
  playerY = (g.blockSize * 3 + g.offsetV1)
  dx = 0
  dy = 0
  gameExit = False
  # main loop
  while not gameExit:
    for event in pygame.event.get():
      # print(event) # DEBUG
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()

      keys = pygame.key.get_pressed()
      # move player
      # X axis
      if keys[pygame.K_LEFT]:
        dx = -playerSpeed
      if keys[pygame.K_RIGHT]:
        dx = playerSpeed

      # Y axis
      if keys[pygame.K_UP]:
        dy = -playerSpeed
      if keys[pygame.K_DOWN]:
        dy = playerSpeed

      # stop location change
      # X axis
      if (keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]) or (not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]):
        dx = 0
      # Y axis
      if (keys[pygame.K_UP] and keys[pygame.K_DOWN]) or (not keys[pygame.K_UP] and not keys[pygame.K_DOWN]):
        dy = 0

    playerX += dx
    playerY += dy

    # gameDisplay.fill(white)
    # if playerX < offsetH1 or playerX > gameWidth - playerWidth:
    #   end()
    # if playerY < offsetV1 or playerY > gameHeight - playerHeight:
    #   end()
    gameDisplay.fill(lightGreen)
    drawFloor()
    showPlayer(playerX, playerY)
    drawMaze(m.levels[0])
    drawGrid()
    # drawImage(wallBlockImg, 1 * g.blockSize, 4 * g.blockSize)
    # drawImage(wallBlockImg, 1 * g.blockSize, math.ceil(5 * g.blockSize))
    # drawImage(wallBlockImg, 2 * g.blockSize, math.ceil(4 * g.blockSize))
    # drawImage(wallBlockImg, 2 * g.blockSize, math.ceil(5 * g.blockSize))
    # drawImage(wallBlockImg, 2 * g.blockSize, math.ceil(6 * g.blockSize))
    # drawImage(wallBlockImg, 3 * g.blockSize, math.ceil(5 * g.blockSize))
    # drawImage(chestImg, 1 * g.blockSize, 1 * g.blockSize, True)
    # sidebar
    pygame.draw.rect(gameDisplay, black, pygame.Rect(g.gameWidth + g.offsetH1 + g.offsetH2, 0, g.sidebarWidth, g.gameFullHeight), 0)
    pygame.display.update()  # update specific thing if specified or whole screen
    clock.tick(60)


gameLoop()
# quit
quit()
