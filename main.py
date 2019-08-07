# imports, init
import pygame
import time
import math

pygame.init()

# variables
# Get real screen resolution 
screenInfo = pygame.display.Info()  # get current screen info
realScreenWidth = screenInfo.current_w  # get width
gameFullWidth = realScreenWidth - 160   # make some offset from screen borders
# gameFullWidth = 1600 - 160
# gameFullWidth = 1366 - 160
# gameFullWidth = 1280 - 160
gameFullHeight = gameWithOffsetHeight = int(round(gameFullWidth * 9 / 16))   # height with some small offsets if screen is not 16*9 resolution
sidebarWidth = int(round(gameFullWidth * .25))  # take 25% (16 * .25 = 4) of game screen for sidebar
gameWithOffsetWidth = gameFullWidth - sidebarWidth  # leave rest for game screen (there also could be some offsets)

cols = 12   # divide all our 12/16 parts of our game screen for columns
rows = 7    # vertical resolution is 9 but we need to reserve two layers for bootom and top layer
gridRows = rows+2   # grid should be drawn for those rows too

offsetH1 = (gameWithOffsetWidth % cols) / 2  # count horizontal offset for left side
offsetH2 = (gameWithOffsetWidth % cols) - offsetH1  # and right too (in case offset should be 3px)
offsetV1 = (gameWithOffsetHeight % gridRows) / 2 # same for vertical left too
offsetV2 = (gameWithOffsetHeight % gridRows) - offsetV1 # and right

# offsetH = 0
# offsetV = 0

gameWidth = gameWithOffsetWidth - (offsetH1 + offsetH2) # define game width that will be used for actual game
gameHeight = gameWithOffsetHeight - (offsetV1 + offsetV2) # same for height

blockSize = gameWidth / cols  # block size = max size of each element in game

playerSpeed = gameWidth / 180 # how much pixels should player move

maze = [ [ 1 if i == 0 or i == cols-1 or j == 0 or j == rows-1 else None for i in range(cols) ] for j in range(rows) ]
# grid[0][0] = 1

print('\n'.join([''.join(['{:5}'.format(item) for item in row])
                 for row in maze]))


black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
lightGreen = (221, 255, 124)

# gameDisplay = pygame.display.set_mode((gameFullWidth,gameHeight),pygame.FULLSCREEN)
gameDisplay = pygame.display.set_mode((gameFullWidth, gameFullHeight))
pygame.display.set_caption('Deep Maze!')
clock = pygame.time.Clock()

playerWidth = int(round(blockSize / 1.29 / 1.3))
playerHeight = int(round(blockSize / 1.3))
playerImg = pygame.transform.scale(
  pygame.image.load("sprites/main-pack/hero/idleA/hero_idleA_0000.png").subsurface(20, 21, 62, 80),
  (playerWidth, playerHeight))
chestImg = pygame.transform.scale(pygame.image.load("sprites/treasure chest/chest1_128.png"),
                                  (int(blockSize * .8), int(blockSize * .8)))  # w:100 h:110
# chestImg = pygame.transform.scale(pygame.image.load("sprites/wk/loot05key.png"),(int(blockSize*1),int(blockSize*1))) # w:100 h:110
# floorBlockImg = pygame.image.load("sprites/main-pack/level/groundEarth_checkered.png")
floorBlockImg = pygame.transform.scale(
  pygame.image.load("sprites/main-pack/level/groundEarth_checkered_7x10.png"),
  (blockSize, blockSize*2))
wallBlockImg = pygame.transform.scale(
  pygame.image.load("sprites/main-pack/level/wallBreakable_7x5+.png"),
  (int(blockSize*1), int(blockSize*1.5)))
# bgImg = pygame.transform.scale(
#     pygame.image.load("sprites/bg.jpg"),
#     (gameWidth, gameHeight))


# code
def showPlayer(x, y):
  drawImage(playerImg,x,y,True)

def drawImage(image, x, y, centered=False):
  # Wall
  if image == wallBlockImg: 
    y += (math.ceil(float(wallBlockImg.get_height()) / float(blockSize)) - (
      float(wallBlockImg.get_height()) / float(blockSize))) * blockSize
    
  if not centered:
    gameDisplay.blit(image, (x + offsetH1, y + offsetV1))
  else:
    localOffsetX = abs((blockSize - image.get_width()) / 2)
    localOffsetY = abs((blockSize - image.get_height()) / 2)
    gameDisplay.blit(image, (x + localOffsetX + offsetH1, y + localOffsetY + offsetV1))


def drawGrid():
  for col in xrange(1, cols):
    pygame.draw.line(gameDisplay, red, (col * blockSize + offsetH1, offsetV1), (col * blockSize + offsetH1, gameHeight), 1)
  for row in xrange(1, gridRows):
    pygame.draw.line(gameDisplay, red, (offsetH1, row * blockSize + offsetV1), (gameWidth, row * blockSize + offsetV1), 1)


def drawFloor():
  for col in xrange(0, cols):
    for row in xrange(1, rows+1):
      gameDisplay.blit(floorBlockImg, (col * blockSize + offsetH1, row * blockSize + offsetV1))


def drawMaze():
  for i in range(rows):
    for j in range(cols):
      if maze[i][j] == 1:
        drawImage(wallBlockImg, j * blockSize, i * blockSize)


def text_objects(text, font):
  textSurface = font.render(text, True, black)
  return textSurface, textSurface.get_rect()


def displayMessage(text):
  largeText = pygame.font.Font('freesansbold.ttf', 115)
  TextSurf, TextRect = text_objects(text, largeText)
  TextRect.center = ((gameWidth / 2), (gameHeight / 2))
  gameDisplay.blit(TextSurf, TextRect)
  pygame.display.update()
  time.sleep(2)
  gameLoop()


def end():
  displayMessage('The end!')


def gameLoop():
  # variables
  drawMaze()
  playerX = (blockSize * 5 + offsetH1)
  playerY = (blockSize * 3 + offsetV1)
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
    drawMaze()
    drawGrid()
    # drawImage(wallBlockImg, 1 * blockSize, 4 * blockSize)
    # drawImage(wallBlockImg, 1 * blockSize, math.ceil(5 * blockSize))
    # drawImage(wallBlockImg, 2 * blockSize, math.ceil(4 * blockSize))
    # drawImage(wallBlockImg, 2 * blockSize, math.ceil(5 * blockSize))
    # drawImage(wallBlockImg, 2 * blockSize, math.ceil(6 * blockSize))
    # drawImage(wallBlockImg, 3 * blockSize, math.ceil(5 * blockSize))
    # drawImage(chestImg, 1 * blockSize, 1 * blockSize, True)
    # sidebar
    pygame.draw.rect(gameDisplay, black, pygame.Rect(gameWidth + offsetH1 + offsetH2, 0, sidebarWidth, gameFullHeight), 0)
    pygame.display.update()  # update specific thing if specified or whole screen
    clock.tick(60)


gameLoop()
# quit
pygame.quit()
quit()
