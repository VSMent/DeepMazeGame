# imports, init
import pygame
import time
pygame.init()


# variables
# Get real screen resolution 
# screenInfo = pygame.display.Info()
# realScreenWidth=screenInfo.current_w
# realScreenHeight=screenInfo.current_h
# TODO: get best resolution for real screen
display_height = 900
display_width = 1600
sidebarWidth = round(display_width * .2)
rightSeparator = display_width - sidebarWidth

black = (0,0,0)
white = (255,255,255)

gameDisplay = pygame.display.set_mode((display_width,display_height))
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
  TextRect.center = ((display_width/2),(display_height/2))
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
    pygame.draw.rect(gameDisplay,black,pygame.Rect(rightSeparator,0,sidebarWidth,display_height),0)
    pygame.display.update() # update specific thing if specified or whole screen
    clock.tick(60)

gameLoop()
# quit
pygame.quit()
quit()




