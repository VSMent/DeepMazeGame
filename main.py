# imports, init
import pygame
import time
pygame.init()


# variables
# Get real screen resolution 
# TODO: get best resolution for real screen
# screenInfo = pygame.display.Info()
# realScreenWidth=screenInfo.current_w
# gameFullWidth = realScreenWidth
# gameFullWidth = 1600
gameFullWidth = 1366
gameHeight = int(round(gameFullWidth * 9/16))
sidebarWidth = int(round(gameFullWidth * .2))
gameWidth = gameFullWidth - sidebarWidth

black = (0,0,0)
white = (255,255,255)

gameDisplay = pygame.display.set_mode((gameFullWidth,gameHeight))
pygame.display.set_caption('Deep Maze!')
clock = pygame.time.Clock()

playerImg = pygame.image.load("sprites/hero/idleA/hero_idleA_0000.png") # w:100 h:110 
playerWidth = 100
playerHeight = 110

#code
def showPlayer(x,y):
  gameDisplay.blit(playerImg,(x,y)) # draw image

def text_objects(text,font):
  textSurface = font.render(text, True, black)
  return textSurface, textSurface.get_rect()

def displayMessage(text):
  largeText = pygame.font.Font('freesansbold.ttf',115)
  TextSurf, TextRect = text_objects(text, largeText)
  TextRect.center = ((gameWidth/2),(gameHeight/2))
  gameDisplay.blit(TextSurf,TextRect)
  pygame.display.update()
  time.sleep(2)
  gameLoop()

def end():
  displayMessage('The end!')  

def gameLoop():
  # variables
  gameExit = False
  # main loop
  while not gameExit:
    for event in pygame.event.get():
      # print(event) # DEBUG
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
           
    gameDisplay.fill(white)
    # showPlayer(playerX,playerY)
    pygame.draw.rect(gameDisplay,black,pygame.Rect(gameWidth,0,sidebarWidth,gameHeight),0)
    pygame.display.update() # update specific thing if specified or whole screen
    clock.tick(60)

gameLoop()
# quit
pygame.quit()
quit()




