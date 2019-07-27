# imports, init
import pygame
import time

pygame.init()

# variables
# Get real screen resolution 
# TODO: get best resolution for real screen
screenInfo = pygame.display.Info()
realScreenWidth = screenInfo.current_w
gameFullWidth = realScreenWidth - 160
# gameFullWidth = 1600 - 160
# gameFullWidth = 1366 - 160
# gameFullWidth = 1280 - 160
gameHeight = int(round(gameFullWidth * 9 / 16))
sidebarWidth = int(round(gameFullWidth * .25))
gameWidth = gameFullWidth - sidebarWidth

playerSpeed = gameWidth / 180
cols = 12
rows = 7
gridRows = 9
blockSize = gameWidth / cols

# startX = (gameWidth - (blockSize * cols)) / 2
# startY = (gameHeight - (blockSize * rows)) / 2
startX = 0
startY = 0

black = (0, 0, 0)
white = (255, 255, 255)

# gameDisplay = pygame.display.set_mode((gameFullWidth,gameHeight),pygame.FULLSCREEN)
gameDisplay = pygame.display.set_mode((gameFullWidth, gameHeight))
pygame.display.set_caption('Deep Maze!')
clock = pygame.time.Clock()

playerWidth = int(round(blockSize / 1.29))
playerHeight = blockSize
playerImg = pygame.transform.scale(
    pygame.image.load("sprites/main-pack/hero/idleA/hero_idleA_0000.png").subsurface(20, 21, 62, 80),
    (playerWidth, playerHeight))
chestImg = pygame.transform.scale(pygame.image.load("sprites/treasure chest/chest1_128.png"),
                                  (int(blockSize * .8), int(blockSize * .8)))  # w:100 h:110
# chestImg = pygame.transform.scale(pygame.image.load("sprites/wk/loot05key.png"),(int(blockSize*1),int(blockSize*1))) # w:100 h:110
# bgBlockImg = pygame.image.load("sprites/main-pack/level/groundEarth_checkered.png")
bgBlockImg = pygame.transform.scale(
    pygame.image.load("sprites/main-pack/level/groundEarth_checkered_7x10.png"),
    (blockSize, blockSize*2))
wallBlockImg = pygame.transform.scale(
    pygame.image.load("sprites/main-pack/level/wallBreakable_7x10.png"),
    (blockSize, int(blockSize*1.5)))


# code
def showPlayer(x, y):
    gameDisplay.blit(playerImg, (x, y))  # draw image


def drawImage(image, x, y, centered=False):
    if not centered:
        gameDisplay.blit(image, (x, y))
    else:
        offsetX = abs((blockSize - image.get_width()) / 2)
        offsetY = abs((blockSize - image.get_height()) / 2)
        gameDisplay.blit(image, (x + offsetX, y + offsetY))


def drawGrid():
    for col in xrange(1, cols):
        pygame.draw.line(gameDisplay, black, (col * blockSize, startY), (col * blockSize, gameHeight), 1)
    for row in xrange(1, gridRows):
        pygame.draw.line(gameDisplay, black, (startX, row * blockSize), (gameWidth, row * blockSize), 1)


def drawBG():
    for col in xrange(0, cols):
        for row in xrange(1, rows+1):
            gameDisplay.blit(bgBlockImg, (col * blockSize + startX, row * blockSize + startY))


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
    playerX = (gameWidth * 0.45)
    playerY = (gameHeight * 0.8)
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

        gameDisplay.fill(white)
        # if playerX < 0 or playerX > gameWidth - playerWidth:
        #   end()
        # if playerY < 0 or playerY > gameHeight - playerHeight:
        #   end()
        drawBG()
        drawGrid()
        showPlayer(playerX, playerY)
        gameDisplay.blit(wallBlockImg, (1 * blockSize + startX, 4.5 * blockSize + startY))
        drawImage(chestImg,  1 * blockSize + startX, 1 * blockSize + startY, True)
        pygame.draw.rect(gameDisplay, black, pygame.Rect(gameWidth, 0, sidebarWidth, gameHeight), 0)
        pygame.display.update()  # update specific thing if specified or whole screen
        clock.tick(60)


gameLoop()
# quit
pygame.quit()
quit()
