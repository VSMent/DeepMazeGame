gameFullWidth = None
gameFullHeight = None
sidebarWidth = None
cols = None
rows = None
gridRows = None
offsetH1 = None
offsetH2 = None
offsetV1 = None
# offsetV2 = None
gameWidth = None
gameHeight = None
blockSize = None
MOVEEVENT = None


def init():
    # in case stuff is not imported
    imp()

    global atexit
    atexit.register(exit)  # register for game exit event

    pygame.init()  # initialize pygame engine

    global gameFullWidth, gameFullHeight, sidebarWidth, gameWidth, gameHeight, blockSize
    global cols, rows, gridRows
    global offsetH1, offsetH2, offsetV1, offsetV2
    global MOVEEVENT

    # Get real screen resolution
    screenInfo = pygame.display.Info()  # get current screen info
    realScreenWidth = screenInfo.current_w  # get width
    # gameFullWidth = realScreenWidth - 160  # make some offset from screen borders
    gameFullWidth = 1200  # make some offset from screen borders
    gameFullHeight = gameWithOffsetHeight = int(
        round(gameFullWidth * 9 / 16))  # height with some small offsets if screen is not 16*9 resolution
    sidebarWidth = int(round(gameFullWidth * .25))  # take 25% (16 * .25 = 4) of game screen for sidebar
    gameWithOffsetWidth = gameFullWidth - sidebarWidth  # leave rest for game screen (there also could be some offsets)

    # Set maze grid
    cols = 12  # divide all our 12/16 parts of our game screen for columns
    rows = 7  # vertical resolution is 9 but we need to reserve two layers for bootom and top empty layers
    gridRows = rows + 2  # grid should be drawn for those rows too

    # Not 16x9 screen fix
    offsetH1 = int((gameWithOffsetWidth % cols) / 2)  # count horizontal offset for left side
    offsetH2 = (gameWithOffsetWidth % cols) - offsetH1  # and right too (in case offset should be 3px)
    offsetV1 = int((gameWithOffsetHeight % gridRows) / 2)  # same for vertical left too
    offsetV2 = (gameWithOffsetHeight % gridRows) - offsetV1  # and right

    # Fixed game resolution
    gameWidth = gameWithOffsetWidth - (offsetH1 + offsetH2)  # define game width that will be used for actual game
    gameHeight = gameWithOffsetHeight - (offsetV1 + offsetV2)  # same for height

    # One cell size
    blockSize = int(gameWidth / cols)  # block size = max size of each element in game

    MOVEEVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(MOVEEVENT, 500)


def imp():
    # import like this so it is visible in other functions
    globals()["pygame"] = __import__("pygame")
    globals()["time"] = __import__("time")
    globals()["math"] = __import__("math")
    globals()["atexit"] = __import__("atexit")


def exit():
    global pygame
    pygame.quit()  # Finish pygame game
