import pygame, random
from Tile import Tile
from Player import Player

pygame.init()

# Size Variables - Screen & Grid
screenX = 500
screenY = 500
row = 20
col = 20
tileSize = (20, 20)
gridXLoc = 50
gridYLoc = 50
textBoxSize = (200, 50)
textBoxXLoc = 50
textBoxYLoc = 250
difficultySetting = 2
score =0
highscore = 0
storeScore =0

# Game Colors
tileColor = (200, 200, 210)
startUpColor = (255, 255, 255)
backgroundColor = (0, 0, 0)
itemColor = (0, 0, 255)
playerColor = (255, 0, 0)
textBoxColor = (0, 0, 0)

# Important Game Objects
clock = pygame.time.Clock()
font = pygame.font.SysFont('georgia', 30)
screen = pygame.display.set_mode((screenX, screenY))
mainPlayer = Player((20, 20), gridXLoc, gridYLoc, 0, tileSize[0])
backgroundImage = pygame.image.load('background.jpg')
pointImage = pygame.image.load('point.png')
pointImage = pygame.transform.scale(pointImage, (101, 31))
collectingSound = pygame.mixer.Sound("collecting.mp3")
themeMusic = pygame.mixer.music.load("musicStuff.mp3")
dataFile = open("data.txt",'r+')

# Lists
grid = [[] for n in range(row)]  # 2D list that stores Tile info
snakeAnimate = []  # list used to animate the snake

# Movement Booleans
isLeft = False
isRight = False
isDown = False
isUp = False
canTurnHorizontal = True
canTurnVertical = True

# Game Booleans
gameRuns = True
gamePlays = True
scene1 = True
scene2 = False
giveScoreInfo = False
optionDisplay = False

# Title and Icon
pygame.display.set_caption("Snake")
gameIcon = pygame.image.load("snake.png")
pygame.display.set_icon(gameIcon)

def getScoreFromFile():
    tempFile = open("data.txt",'r')
    data = (tempFile.readlines())[0]
    tempNum = data.index("-")
    highscore = int(data[tempNum+1:])
    tempFile.close()
    return highscore

def sendScoreToFile():
    tempFile = open("data.txt",'w')
    tempFile.write("Highscore-"+str(highscore))
    tempFile.close()

def writeText(msg, color, x, y):
    text = font.render(msg, True, color)
    screen.blit(text, (x, y))


# Traverses 2D list to fill with Tile Object
def createGameGrid():
    for x in range(row):
        for y in range(col):
            grid[x].append(Tile(tileColor, tileSize, False, False, False))


# Find a random tile to give an Item to
def giveRandItem():
    given = False
    while not (given):
        randXNum = random.randint(0, row - 1)
        randYNum = random.randint(0, col - 1)
        if not (grid[randXNum][randYNum].hasPlayer):
            grid[randXNum][randYNum].hasItem = True
            given = True


# Draws all the tiles
def drawAllRect():
    global score, highscore
    xTemp = gridXLoc
    yTemp = gridYLoc
    for x in range(row):
        for y in range(col):
            pygame.draw.rect(screen, grid[x][y].color, (xTemp, yTemp, grid[x][y].size[0], grid[x][y].size[1]), 0, 5)
            if grid[x][y].hasItem:
                pygame.draw.rect(screen, itemColor, (xTemp, yTemp, grid[x][y].size[0], grid[x][y].size[1]), 0, 5)
            if grid[x][y].hasPlayer:
                pygame.draw.rect(screen, playerColor, (xTemp, yTemp, grid[x][y].size[0], grid[x][y].size[1]), 0, 5)
            yTemp += grid[x][y].size[1]
        yTemp = gridYLoc
        xTemp += grid[x][y].size[0]
    writeText("Score: "+ str(score),textBoxColor,340,20)
    writeText(" High Score: " + str(highscore), textBoxColor, 50, 20)

# use before the gameRun while loop to set up
def setUpGame():
    createGameGrid()
    giveRandItem()


def drawPlayer():
    pygame.draw.rect(screen, playerColor, (mainPlayer.locX, mainPlayer.locY, tileSize[0], tileSize[1]), 0, 5)


def updatePlayer():
    # double if loop logic to control player movement
    if isLeft:
        # allows the snake to go from one side to another, similar logic is used for other directions too
        if mainPlayer.locX <= gridXLoc:
            mainPlayer.locX = gridXLoc + tileSize[0] * row  # -mainPlayer.body[0]
        mainPlayer.locX -= mainPlayer.dX
    if isRight:
        if mainPlayer.locX >= gridXLoc + tileSize[0] * row - mainPlayer.body[0]:
            mainPlayer.locX = gridXLoc - mainPlayer.body[0]
        mainPlayer.locX += mainPlayer.dX
    if isUp:
        if mainPlayer.locY <= gridYLoc:
            mainPlayer.locY = gridYLoc + tileSize[1] * col
        mainPlayer.locY -= mainPlayer.dX
    if isDown:
        if mainPlayer.locY >= gridYLoc + tileSize[1] * row - mainPlayer.body[1]:
            mainPlayer.locY = gridYLoc - mainPlayer.body[1]
        mainPlayer.locY += mainPlayer.dX
    # used to animate the snake, removes the player from the squares behind it to show movement
    if len(snakeAnimate) > mainPlayer.length:
        tempRow = (snakeAnimate[0])[0]
        tempCol = (snakeAnimate[0])[1]
        grid[tempRow][tempCol].hasPlayer = False
        grid[tempRow][tempCol].canEndGame = False
        snakeAnimate.pop(0)


# finds the player position in the grid list based on its pixel location
def locatePlayer():
    global score
    tempXLoc = mainPlayer.locX
    tempYLoc = mainPlayer.locY
    tempRow = (int)((tempXLoc - gridXLoc) / tileSize[0])
    tempCol = (int)((tempYLoc - gridYLoc) / tileSize[1])
    grid[tempRow][tempCol].hasPlayer = True
    if grid[tempRow][tempCol].canEndGame:
        return False
        print("GAME OVER")
    snakeAnimate.append((tempRow, tempCol))
    if grid[tempRow][tempCol].hasItem:
        collectingSound.play()
        score+=1
        grid[tempRow][tempCol].hasItem = False
        mainPlayer.length += 1
        giveRandItem()
    grid[tempRow][tempCol].canEndGame = True
    return True


def startUpScreen():
    global scene1, scene2, optionDisplay, difficultySetting, giveScoreInfo, storeScore, highscore
    writeText("PLAY GAME", (0, 0, 0), textBoxXLoc, textBoxYLoc)
    writeText("Option", (0, 0, 0), textBoxXLoc, textBoxYLoc + 50)
    tempPos = pygame.mouse.get_pos()
    tempX = tempPos[0]
    tempY = tempPos[1]
    if event.type == pygame.MOUSEBUTTONDOWN and tempX > textBoxXLoc and tempX < textBoxXLoc + 180 and tempY > textBoxYLoc and tempY < textBoxYLoc + 50:
        scene1 = False
        scene2 = True
    if tempX > textBoxXLoc and tempX < textBoxXLoc + 90 and tempY > textBoxYLoc+50 and tempY < textBoxYLoc + 80:
        writeText("Option", (255, 0, 0), textBoxXLoc, textBoxYLoc + 50)
        optionDisplay = True
    if optionDisplay:
        writeText("Option", (255, 0, 0), textBoxXLoc, textBoxYLoc + 50)
        screen.blit(pointImage, (textBoxXLoc + 65, textBoxYLoc + 55))
        screen.blit(pointImage, (textBoxXLoc + 65, textBoxYLoc + 105))
        screen.blit(pointImage, (textBoxXLoc + 65, textBoxYLoc + 155))
        writeText("Easy", (0, 0, 0), textBoxXLoc + 140, textBoxYLoc + 55)
        writeText("Medium", (0, 0, 0), textBoxXLoc + 140, textBoxYLoc + 105)
        writeText("Hard", (0, 0, 0), textBoxXLoc + 140, textBoxYLoc + 155)
        if tempX > textBoxXLoc +140 and tempX < textBoxXLoc + 205 and tempY > textBoxYLoc + 55 and tempY < textBoxYLoc + 90:
            writeText("Easy", (255, 0, 0), textBoxXLoc + 140, textBoxYLoc + 55)
            if event.type == pygame.MOUSEBUTTONDOWN:
                optionDisplay = False
                difficultySetting = 1  # Easy mode
        if tempX > textBoxXLoc +140 and tempX < textBoxXLoc + 250 and tempY > textBoxYLoc + 105 and tempY < textBoxYLoc + 140:
            writeText("Medium", (255, 0, 0), textBoxXLoc + 140, textBoxYLoc + 105)
            if event.type == pygame.MOUSEBUTTONDOWN:
                optionDisplay = False
                difficultySetting = 2  # Medium mode
        if tempX > textBoxXLoc +140 and tempX < textBoxXLoc + 205 and tempY > textBoxYLoc + 155 and tempY < textBoxYLoc + 190:
            writeText("Hard", (255, 0, 0), textBoxXLoc + 140, textBoxYLoc + 155)
            if event.type == pygame.MOUSEBUTTONDOWN:
                optionDisplay = False
                difficultySetting = 2.5  # Hard mode
    if giveScoreInfo:
        writeText("Score: " + str(storeScore), (0, 0, 0), textBoxXLoc + 200, textBoxYLoc + 55)
        writeText("HighScore: "+ str(highscore), (0, 0, 0), textBoxXLoc + 200, textBoxYLoc + 105)

def resetGame():
    global grid, scene1, mainPlayer, snakeAnimate, isLeft, isRight, isDown, isUp, canTurnHorizontal, canTurnVertical, score
    scene1 = True
    score =0
    grid = [[] for n in range(row)]
    snakeAnimate = []
    mainPlayer.length = 0
    mainPlayer.locY = gridYLoc
    mainPlayer.locX = gridXLoc
    isLeft = False
    isRight = False
    isDown = False
    isUp = False
    canTurnHorizontal = True
    canTurnVertical = True
    setUpGame()


setUpGame()
highscore = getScoreFromFile()
getScoreFromFile()
pygame.mixer.music.play(-1)
while gameRuns:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRuns = False
        if event.type == pygame.KEYDOWN and scene2:
            if event.key == pygame.K_LEFT and canTurnHorizontal:
                isLeft = True
                isRight = False
                isUp = False
                isDown = False
                canTurnHorizontal = False
                canTurnVertical = True
            if event.key == pygame.K_RIGHT and canTurnHorizontal:
                isLeft = False
                isRight = True
                isUp = False
                isDown = False
                canTurnHorizontal = False
                canTurnVertical = True
            if event.key == pygame.K_UP and canTurnVertical:
                isLeft = False
                isRight = False
                isUp = True
                isDown = False
                canTurnHorizontal = True
                canTurnVertical = False
            if event.key == pygame.K_DOWN and canTurnVertical:
                isLeft = False
                isRight = False
                isUp = False
                isDown = True
                canTurnHorizontal = True
                canTurnVertical = False
    screen.fill(startUpColor)
    screen.blit(backgroundImage, (0, 0))
    if scene1:
        startUpScreen()
    if scene2:
        drawAllRect()
        drawPlayer()
        scene2 = locatePlayer()
        if scene2 == False:
            giveScoreInfo= True
            if score>=highscore:
                highscore=score
                sendScoreToFile()
            storeScore = score
            resetGame()
        updatePlayer()

    pygame.display.update()
    clock.tick(8 * difficultySetting)
