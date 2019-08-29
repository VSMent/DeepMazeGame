import random
import time

class Maze:
  """
  Data structure for generating and storing all maze related variables

  Maze level pattern:
  cell: 221 - player,exit,grass
  background - digit place 0 (just for bg)
    1 - background grass
  midground - digit place 1 (player can interract (stand on them))
    1 - foreground void
    2 - foreground exit
  foreground - digit place 2 (player can't stand on same spot)
    1 - foreground wall
    2 - foreground player
  """
  def __init__(self, cols,rows,size):
    self.patternBgDigit=0
    self.patternBgGrass=1
    self.patternMgDigit=1
    self.patternMgVoid=1
    self.patternMgExit=2
    self.patternFgDigit=2
    self.patternFgWall=1
    self.patternFgPlayer=2
    self.levels = []
    self.cols = cols
    self.rows = rows
    self.size = size
    self.gridRows = rows+2
    self.initialPlayerPos=()
    self.exitPoint=()
    self.walkableFgObjects = (self.patternMgVoid,self.patternMgExit)
    random.seed(int(time.time()))

  def generateMaze(self,level = 0): #complexity level
    self.levels.append(
      [[(self.patternFgWall*10**(self.patternFgDigit)) if i == 0 or i == self.cols - 1 or j == 0 or j == self.rows - 1 else (self.patternMgVoid*10**(self.patternMgDigit)) for i in range(self.cols)] for j in range(self.rows)]
    ) # basic pattern (walls around the map)
    # place player
    self.initialPlayerPos = (random.randrange(1,self.rows-1,1),random.randrange(1,self.cols-1,1))
    self.levels[level][self.initialPlayerPos[0]][self.initialPlayerPos[1]] += self.patternFgPlayer*10**(self.patternFgDigit)
    # pick end point (random, longest path?)
    # self.exitPoint = (random.randrange(1,self.rows-1,1),random.randrange(1,self.cols-1,1))
    self.exitPoint = (1,1)
    self.levels[level][self.exitPoint[0]][self.exitPoint[1]] = self.patternMgExit*10**(self.patternMgDigit)
# 1  1  1  1  1  1  1  1  1  1  1  1
# 1  10 10 10 10 10 10 10 10 10 10 1
# 1  10 10 10 10 10 10 10 10 10 10 1
# 1  10 10 10 10 10 10 10 10 10 10 1
# 1  10 10 10 10 10 10 10 10 10 10 1
# 1  10 10 10 10 10 10 10 10 10 10 1
# 1  1  1  1  1  1  1  1  1  1  1  1

  def showMazeMap(self,level=0):
    print('\n'+'\n'.join([''.join(['{!s:5}'.format(item) for item in row])
                 for row in self.levels[level]]))