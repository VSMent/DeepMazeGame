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
    random.seed(int(time.time()))

  def generateMaze(self,level = 0): #complexity level
    self.levels.append(
      [[1 if i == 0 or i == self.cols - 1 or j == 0 or j == self.rows - 1 else None for i in range(self.cols)] for j in range(
        self.rows)]
    ) # basic pattern (walls around the map)
