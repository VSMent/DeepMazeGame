# imports
import pygame

#variables
display_width = 800
display_height = 600


black = (0,0,0)
white = (255,255,255)

#code
pygame.init()
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Deep Maze!')
clock = pygame.time.Clock()
playerImg = pygame.image.load("sprites/hero/idleA/hero_idleA_0000.png") # w:100 h:110 

def showPlayer(x,y):
  gameDisplay.blit(playerImg,(x,y)) # draw image

playerX = (display_width * 0.45)
playerY = (display_height * 0.8)



isEnd = False
# main loop
while not isEnd:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      isEnd = True
    # print(event) # DEBUG
  gameDisplay.fill(white)
  showPlayer(playerX,playerY)

  pygame.display.update() # update specific thing if specified or whole screen
  clock.tick(60)

# quit
pygame.quit()
quit()




