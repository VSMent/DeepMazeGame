# imports, init
import pygame
import time
pygame.init()

#variables
display_width = 800
display_height = 600

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
  playerX = (display_width * 0.45)
  playerY = (display_height * 0.8)
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
        dx = -5
      if keys[pygame.K_RIGHT]:
        dx = 5
          
      # Y axis
      if keys[pygame.K_UP]:
        dy = -5
      if keys[pygame.K_DOWN]:
        dy = 5

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
    if playerX < 0 or playerX > display_width - playerWidth:
      end()
    if playerY < 0 or playerY > display_height - playerHeight:
      end()
    showPlayer(playerX,playerY)

    pygame.display.update() # update specific thing if specified or whole screen
    clock.tick(60)

gameLoop()
# quit
pygame.quit()
quit()




