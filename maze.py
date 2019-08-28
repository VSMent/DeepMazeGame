import random
import time

class Maze:
  """
  Data structure for generating and storing all maze related variables

  Maze level pattern:
  cell: 12 - grass,player
  foreground - digit place 0 
    1  - foreground wall
    2  - foreground player
  background - digit place 1
    1 - background grass
  """
  def __init__(self, cols,rows,size):
    self.patternFgDigit=0
    self.patternFgWall=1
    self.patternFgPlayer=2
    self.patternBgDigit=1
    self.patternBgGrass=1
    self.levels = []
    self.cols = cols
    self.rows = rows
    self.size = size
    self.gridRows = rows+2
    self.initialPlayerPos=()
    random.seed(int(time.time()))

  def generateMaze(self,level = 0): #complexity level
    self.levels.append(
      # [[1 if i == 0 or i == self.cols - 1 or j == 0 or j == self.rows - 1 else None for i in range(self.cols)] for j in range(self.rows)]
      [[1 if i == 0 or i == self.cols - 1 or j == 0 or j == self.rows - 1 else 10 for i in range(self.cols)] for j in range(self.rows)]
    ) # basic pattern (walls around the map)
    # place player
    # random.randrange(1,self.cols-2,1) from_including, to_excluding, step
    self.initialPlayerPos = (random.randrange(1,self.rows-1,1),random.randrange(1,self.cols-1,1))
    # self.levels[level][3][3]=1
    # print(len(self.levels),level,
    #   "\n",self.rows,self.initialPlayerPos[0],
    #   "\n",self.cols,self.initialPlayerPos[1])
    # self.levels[level][self.initialPlayerPos[0]][self.initialPlayerPos[1]] = 2
    self.levels[level][self.initialPlayerPos[0]][self.initialPlayerPos[1]] += self.patternFgPlayer
    # pick end point
# 1    1    1    1    1    1    1    1    1    1    1    1
# 1    None None None None None None None None None None 1
# 1    None None None None None None None None None None 1
# 1    None None None None None None None None None None 1
# 1    None None None None None None None None None None 1
# 1    None None None None None None None None None None 1
# 1    1    1    1    1    1    1    1    1    1    1    1

  def showMazeMap(self,level=0):
    print('\n'.join([''.join(['{!s:3}'.format(item) for item in row])
                 for row in self.levels[level]]))