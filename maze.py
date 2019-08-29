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

    def __init__(self):
        self.patternBgDigit = 0
        self.patternBgGrass = 1
        self.patternMgDigit = 1
        self.patternMgVoid = 1
        self.patternMgExit = 2
        self.patternFgDigit = 2
        self.patternFgWall = 1
        self.patternFgPlayer = 2
        self.currentLevel = 0
        self.goToNextLevel = False
        self.levels = []
        self.cols = 0
        self.rows = 0
        self.initialPlayerPos = ()
        self.exitPoint = ()
        self.walkableFgObjects = (self.patternMgVoid, self.patternMgExit)
        random.seed(int(time.time()))

    def generate_maze(self, rows, cols, level=0):  # complexity level
        self.rows = rows
        self.cols = cols
        self.levels.append(
            [[(self.patternFgWall * 10 ** (
                self.patternFgDigit)) if i == 0 or i == self.cols - 1 or j == 0 or j == self.rows - 1 else (
                    self.patternMgVoid * 10 ** self.patternMgDigit) for i in range(self.cols)] for j in
             range(self.rows)]
        )  # basic pattern (walls around the map)
        # place player
        self.initialPlayerPos = (random.randrange(1, self.rows - 1, 1), random.randrange(1, self.cols - 1, 1))
        self.levels[level][self.initialPlayerPos[0]][self.initialPlayerPos[1]] += self.patternFgPlayer * 10 ** (
            self.patternFgDigit)
        # pick end point (random, longest path?)
        self.exitPoint = (random.randrange(1, self.rows - 1, 1), random.randrange(1, self.cols - 1, 1))
        while self.exitPoint == self.initialPlayerPos or abs(self.exitPoint[0]-self.initialPlayerPos[0]) < 2 or abs(self.exitPoint[1]-self.initialPlayerPos[1]) < 2:
            self.exitPoint = (random.randrange(1, self.rows - 1, 1), random.randrange(1, self.cols - 1, 1))
        self.levels[level][self.exitPoint[0]][self.exitPoint[1]] = self.patternMgExit * 10 ** self.patternMgDigit

    # 1  1  1  1  1  1  1  1  1  1  1  1
    # 1  10 10 10 10 10 10 10 10 10 10 1
    # 1  10 10 10 10 10 10 10 10 10 10 1
    # 1  10 10 10 10 10 10 10 10 10 10 1
    # 1  10 10 10 10 10 10 10 10 10 10 1
    # 1  10 10 10 10 10 10 10 10 10 10 1
    # 1  1  1  1  1  1  1  1  1  1  1  1

    def show_maze_level(self, level=0):
        print("\nL: {}".format(level))
        print('\n'.join([''.join(['{!s:5}'.format(item) for item in row])
                        for row in self.levels[level]]))

    def show_all_maze_levels(self):
        i = 0
        while i < len(self.levels):
            self.show_maze_level(i)
            i += 1
