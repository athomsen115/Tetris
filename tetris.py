import pygame, random
import tkinter as tk
from tkinter import messagebox

"""
10 x 20 square Grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 -6
"""

pygame.font.init()

#Global Variables
WIDTH = 800
HEIGHT = 700
PLAY_WIDTH = 300  # meaning 300 // 10 = 30 width per block
PLAY_HEIGHT = 600 # meaning 600 // 20 = 20 height per block
BLOCK_SIZE = 30

TOP_LEFT_X = (WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = HEIGHT - PLAY_HEIGHT

# SHAPES
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
      ['.....',
       '..0..',
       '..00.',
       '...0.',
       '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
      ['.....',
       '..0..',
       '.00..',
       '.0...',
       '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
      ['.....',
       '0000.',
       '.....',
       '.....',
       '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
      ['.....',
       '..00.',
       '..0..',
       '..0..',
       '.....'],
      ['.....',
       '.....',
       '.000.',
       '...0.',
       '.....'],
      ['.....',
       '..0..',
       '..0..',
       '.00..',
       '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
      ['....',
       '..0..',
       '..0..',
       '..00.',
       '.....'],
      ['.....',
       '.....',
       '.000.',
       '.0...',
       '.....'],
      ['.....',
       '.00..',
       '..0..',
       '..0..']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
      ['.....',
       '..0..',
       '..00.',
       '..0..',
       '.....'],
      ['.....',
       '.....',
       '.000.',
       '..0..',
       '.....'],
      ['.....',
       '..0..',
       '.00..',
       '..0..',
       '.....']]

GREEN = (0, 255, 0)
RED = (255, 0, 0)
LBLUE = (0, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

shapes = [S, Z, I, O, J, L, T]  #index 0-6 to represent the different shapes, which correspond with the following colors
shapeColors = [GREEN, RED, LBLUE, YELLOW, ORANGE, BLUE, PURPLE]

class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shapeColors[shapes.index(shape)]
        self.rotation = 0

def createGrid(locked_pos = {}):
    grid = [[BLACK for _ in range(10)] for _ in range(20)]
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c
    return grid

def convertShapeFormat(shape):
    positions = []
    shapes = shape.shape[shape.rotation % len(shape.shape)]
    
    for i, line in enumerate(shapes):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x +j, shape.y + i))
    
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    
    return positions

def validSpace(shape, grid):
    accepted_pos = [[(j,i) for j in range(10) if grid[i][j] == BLACK] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]
    
    formatted = convertShapeFormat(shape)
    
    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True
     

def checkLost(positions):
    for pos in positions:
        _, y = pos
        if y < 1:
            return True
    return False

def getShape():
    return Piece(5, 0, random.choice(shapes))

def drawText(surface, text, size, color):
    font = pygame.font.SysFont('comicsans', size, bold = True)
    label = font.render(text, 1, color)
    
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH/2 - (label.get_width()/2), TOP_LEFT_Y + PLAY_HEIGHT/2 - (label.get_height()/2)))

def updateScore(newscore):
    score = maxScore()
        
    with open('scores.txt', 'w') as f:
        if int(score) > newscore:
            f.write(str(score))
        else:
            f.write(str(newscore))
            message_box("High Score", "NEW HIGH SCORE!!!")
            
def maxScore():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
        
    return score

def drawGrid(surface, grid):
    sx = TOP_LEFT_X
    sy = TOP_LEFT_Y
    
    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*BLOCK_SIZE), (sx + PLAY_WIDTH, sy + i*BLOCK_SIZE))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128,128,128), (sx + j*BLOCK_SIZE, sy), (sx + j*BLOCK_SIZE, sy + PLAY_HEIGHT))
    

def clearRows(grid, locked):
    inc = 0
    
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
                
    if inc > 0:
        for key in sorted(list(locked), key = lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    
    return inc
                

def drawNextShape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape:', 1, WHITE)
    
    sx = TOP_LEFT_X + PLAY_WIDTH + 50
    sy = TOP_LEFT_Y + PLAY_HEIGHT/2 - 100
    
    shapes = shape.shape[shape.rotation % len(shape.shape)]
    
    for i, line in enumerate(shapes):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*BLOCK_SIZE, sy + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                
    surface.blit(label, (sx + 10, sy - 30))
    

def drawGame(surface, grid, score = 0, lastScore = 0):
    surface.fill(BLACK)
    bg = pygame.image.load('tetrisBackground.jpg')
    surface.blit(bg, (0, 0))
    
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, WHITE)
    
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH/2 - label.get_width()/2, 30))
    
    #current score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, WHITE)
    
    sx = TOP_LEFT_X + PLAY_WIDTH + 50
    sy = TOP_LEFT_Y + PLAY_HEIGHT/2 - 100
    
    surface.blit(label, (sx + 20, sy + 150)) 
    
    #High Score
    label = font.render('High Score: ' + str(lastScore), 1, WHITE)
    
    sx = TOP_LEFT_X - 200
    sy = TOP_LEFT_Y + PLAY_HEIGHT/2 - 100
    
    surface.blit(label, (sx + 20, sy + 150))
        
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (TOP_LEFT_X + j*BLOCK_SIZE, TOP_LEFT_Y + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            
    pygame.draw.rect(surface, (255, 0, 0), (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)
    
    drawGrid(surface, grid)
    #pygame.display.update()

def main(win):
    lastScore = maxScore()
    lockedPositions = {}
    grid = createGrid(lockedPositions)
    
    changePiece = False
    run = True
    currentPiece = getShape()
    nextPiece = getShape()
    clock = pygame.time.Clock()
    fallTime = 0
    fallSpeed = 0.27
    levelTime = 0
    score = 0
    
    while run:
        grid = createGrid(lockedPositions)
        fallTime += clock.get_rawtime()
        levelTime += clock.get_rawtime()
        clock.tick()
        
        if levelTime/1000 > 5:
            levelTime = 0
            if fallSpeed > 0.12:
                fallSpeed -= 0.005
    
        if fallTime/1000 > fallSpeed:
            fallTime = 0
            currentPiece.y += 1
            if not(validSpace(currentPiece, grid)) and currentPiece.y > 0:
                currentPiece.y -= 1
                changePiece = True
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    currentPiece.x -= 1
                    if not(validSpace(currentPiece, grid)):
                        currentPiece.x += 1
                if event.key == pygame.K_RIGHT:
                    currentPiece.x += 1
                    if not(validSpace(currentPiece, grid)):
                        currentPiece.x -= 1
                if event.key == pygame.K_DOWN:
                    currentPiece.y += 1
                    if not(validSpace(currentPiece, grid)):
                        currentPiece.y -= 1
                if event.key == pygame.K_UP:
                    currentPiece.rotation += 1
                    if not(validSpace(currentPiece, grid)):
                        currentPiece.rotation -= 1
         
        shapePos = convertShapeFormat(currentPiece)
        
        for i in range(len(shapePos)):
            x, y = shapePos[i]
            if y > -1:
                grid[y][x] = currentPiece.color
                
        if changePiece:
            for pos in shapePos:
                p = (pos[0], pos[1])
                lockedPositions[p] = currentPiece.color
            currentPiece = nextPiece
            nextPiece = getShape()
            changePiece = False
            score += clearRows(grid, lockedPositions) * 10       
        
        drawGame(win, grid, score, lastScore)
        drawNextShape(nextPiece, win)
        pygame.display.update()
        
        if checkLost(lockedPositions):
            pygame.time.delay(1500)
            run = False
            updateScore(score)
            lossScreen(score)
            #pygame.display.update()

def lossScreen(score):
    lossFont = pygame.font.SysFont('comicsans', 80)
    smallFont = pygame.font.SysFont('comicsans', 60)
    lostTxt = 'You Lost...'
    againTxt = "Press any key to play again!"
    sadTetris = pygame.image.load("sadTetris.png")
    pygame.time.delay(1000)
    win.fill(RED)
    
    label = lossFont.render(lostTxt, 1, BLACK)
    againLabel = smallFont.render(againTxt, 1, GREEN)
    scoreLabel = smallFont.render("Last Score: " + str(score), 1, WHITE)
    highScore = smallFont.render("High Score: " + maxScore(), 1, WHITE)
    
    win.blit(label, ((WIDTH/2 - label.get_width()/2), (100 - label.get_height()/2)))
    win.blit(sadTetris, (WIDTH/2 - sadTetris.get_width()/2, HEIGHT/2 - sadTetris.get_height()/2))
    win.blit(scoreLabel, (WIDTH/2 - scoreLabel.get_width() - 40, 500))
    win.blit(highScore, (WIDTH/2 + highScore.get_width()/4, 500))
    win.blit(againLabel, (WIDTH/2 - againLabel.get_width()/2, 625))
    
    pygame.display.update()
    again = True
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                again = False
                main(win)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def mainMenu(win):
    run = True
    while run:
        win.fill(LBLUE)
        tetris = pygame.image.load('tetris.jpg')
        win.blit(tetris, (0,0))
        
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render('Press Any Key to Play', 1, WHITE)
        
        win.blit(label, (WIDTH/2 - label.get_width()/2, 550))
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)
                
    pygame.display.quit()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tetris')
mainMenu(win)


