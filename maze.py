import random
import time

class Maze:
  """
  Data structure for generating and storing all maze related variables
  """
  def __init__(self, cols,rows,size):
    self.levels = []
    self.cols = cols
    self.rows = rows
    self.size = size
    self.gridRows = rows+2
    self.initialPlayerPos=()
    random.seed(int(time.time()))

  def generateMaze(self,level = 0): #complexity level
    self.levels.append(
      [[1 if i == 0 or i == self.cols - 1 or j == 0 or j == self.rows - 1 else None for i in range(self.cols)] for j in range(self.rows)]
    ) # basic pattern (walls around the map)
    # place player
    # random.randrange(1,self.cols-2,1) from_including, to_excluding, step
    self.initialPlayerPos = (random.randrange(1,self.rows-1,1),random.randrange(1,self.cols-1,1))
    # print(len(self.levels),level,
    #   "\n",self.rows,self.initialPlayerPos[0],
    #   "\n",self.cols,self.initialPlayerPos[1])
    # self.levels[level][self.initialPlayerPos[0]][self.initialPlayerPos[1]] = 2
    self.levels[level][self.initialPlayerPos[0]][self.initialPlayerPos[1]] = 2
    # pick end point
# 1    1    1    1    1    1    1    1    1    1    1    1
# 1    None None None None None None None None None None 1
# 1    None None None None None None None None None None 1
# 1    None None None None None None None None None None 1
# 1    None None None None None None None None None None 1
# 1    None None None None None None None None None None 1
# 1    1    1    1    1    1    1    1    1    1    1    1