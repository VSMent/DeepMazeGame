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
      1 - midground void
      2 - midground exit
    foreground - digit place 2 (player can't stand on same spot)
      1 - foreground wall
      2 - foreground player
    """

    def __init__(self):
        """
        Define main variables
        """
        # define maze object integers and digits
        self.patternBgDigit = 0
        self.patternBgGrass = 1
        self.patternMgDigit = 1
        self.patternMgVoid = 1
        self.patternMgExit = 2
        self.patternFgDigit = 2
        self.patternFgWall = 1
        self.patternFgPlayer = 2
        self.currentLevel = 0

        self.levels = []  # all maze levels
        # TODO: make it function temp variable
        self.initialPlayerPos = ()  # player initial coordinates for current level
        # TODO: make it function temp variable
        self.exitPoint = ()  # exit initial coordinates for current level
        self.walkableMgObjects = (self.patternMgVoid, self.patternMgExit)  # walkable objects on mid layer
        random.seed(int(time.time()))  # initialize random random

    def generate_maze(self, rows, cols):  # complexity level
        """
        Generate maze level
        :param rows: int, height of the maze
        :param cols: int, width of the maze
        """
        self.levels.append(
            [[(self.patternFgWall * 10 ** (
                self.patternFgDigit)) if i == 0 or i == cols - 1 or j == 0 or j == rows - 1 else (
                    self.patternMgVoid * 10 ** self.patternMgDigit) for i in range(cols)] for j in
             range(rows)]
        )  # add new level with basic pattern (walls around the map)
        # set random player coordinates
        self.initialPlayerPos = (random.randrange(1, rows - 1, 1), random.randrange(1, cols - 1, 1))
        # set player on maze matrix
        self.levels[self.currentLevel][self.initialPlayerPos[0]][self.initialPlayerPos[1]] += self.patternFgPlayer * 10 ** self.patternFgDigit
        # pick end point (random, longest path?)
        # TODO: make it not just random, but more complex
        # set random exit coordinates
        self.exitPoint = (random.randrange(1, rows - 1, 1), random.randrange(1, cols - 1, 1))
        while self.exitPoint == self.initialPlayerPos or abs(self.exitPoint[0]-self.initialPlayerPos[0]) < 2 or abs(self.exitPoint[1]-self.initialPlayerPos[1]) < 2:
            # set random point again if it is in 1 cell near player
            self.exitPoint = (random.randrange(1, rows - 1, 1), random.randrange(1, cols - 1, 1))
        # set player on maze matrix
        self.levels[self.currentLevel][self.exitPoint[0]][self.exitPoint[1]] = self.patternMgExit * 10 ** self.patternMgDigit

    def print_maze_level(self, level=0):
        """
        Debug, print any generated maze level
        :param level: int, level number starting from 0
        """
        print("\nL: {}".format(level))
        print('\n'.join([''.join(['{!s:5}'.format(item) for item in row])
                        for row in self.levels[self.currentLevel]]))

    def print_all_maze_levels(self):
        """
        Debug, print all maze levels
        """
        i = 0
        while i < len(self.levels):
            self.print_maze_level(i)
            i += 1
