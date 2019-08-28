import random
import time

class Maze:
  """
  Data structure for generating and storing all maze related variables

  Maze level pattern:
  cell: 12 - grass,player
  foreground - digit place 0 
    0 - foreground void
    1 - foreground wall
    2 - foreground player
    3 - foreground exit
  background - digit place 1
    1 - background grass
  """
  def __init__(self, cols,rows,size):
    self.patternFgDigit=0
    self.patternFgVoid=0
    self.patternFgWall=1
    self.patternFgPlayer=2
    self.patternFgExit=3
    self.patternBgDigit=1
    self.patternBgGrass=1
    self.levels = []
    self.cols = cols
    self.rows = rows
    self.size = size
    self.gridRows = rows+2
    self.initialPlayerPos=()
    self.exitPoint=()
    random.seed(int(time.time()))

  def generateMaze(self,level = 0): #complexity level
    self.levels.append(
      [[1 if i == 0 or i == self.cols - 1 or j == 0 or j == self.rows - 1 else 10 for i in range(self.cols)] for j in range(self.rows)]
    ) # basic pattern (walls around the map)
    # place player
    self.initialPlayerPos = (random.randrange(1,self.rows-1,1),random.randrange(1,self.cols-1,1))
    self.levels[level][self.initialPlayerPos[0]][self.initialPlayerPos[1]] += self.patternFgPlayer
    # pick end point (random, longest path?)
    # self.exitPoint = (random.randrange(1,self.rows-1,1),random.randrange(1,self.cols-1,1))
    self.exitPoint = (1,1)
    self.levels[level][self.exitPoint[0]][self.exitPoint[1]] = self.patternFgExit
# 1  1  1  1  1  1  1  1  1  1  1  1
# 1  10 10 10 10 10 10 10 10 10 10 1
# 1  10 10 10 10 10 10 10 10 10 10 1
# 1  10 10 10 10 10 10 10 10 10 10 1
# 1  10 10 10 10 10 10 10 10 10 10 1
# 1  10 10 10 10 10 10 10 10 10 10 1
# 1  1  1  1  1  1  1  1  1  1  1  1

  def showMazeMap(self,level=0):
    print('\n'.join([''.join(['{!s:3}'.format(item) for item in row])
                 for row in self.levels[level]]))