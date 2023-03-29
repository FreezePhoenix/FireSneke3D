import pygame, sys, random, math
from pygame.locals import *

pygame.init()
SCORE = 0
WINDOWW = 800
WINDOWH = 800
WAIT = 100
IS_GAMEOVER = False
DISPLAYSURF = pygame.display.set_mode((WINDOWW, WINDOWH))
fpsClock = pygame.time.Clock()
boxSize = 10
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
FONT_OBJ = pygame.font.Font('freesansbold.ttf', boxSize*2)

pygame.display.set_caption('Fire Snake')
class Snake():
    def __init__(self):
            self.segments = [
              Location(4,2),
              Location(3,2),
              Location(2,2)
            ]
            self.direction = "right"
            self.nextDirection = "right"
    
    def draw(self):
        for segment in self.segments:
            index = self.segments.index(segment)
            color = ((255-(255/(len(self.segments))*index)), 0, 0)
            rect = pygame.Rect(segment.x * boxSize,segment.y * boxSize, boxSize, boxSize)
            pygame.draw.rect(DISPLAYSURF, color, rect)
    def move(self):
        head = self.segments[0]
        
        self.direction = self.nextDirection
        direction = self.direction
        if direction == "right":
            self.segments = [Location(head.x+1,head.y)]+self.segments
        elif direction == "left":
            self.segments = [Location(head.x-1,head.y)]+self.segments
        elif direction == "up":
            self.segments = [Location(head.x,head.y-1)]+self.segments
        elif direction == "down":
            self.segments = [Location(head.x,head.y+1)]+self.segments
        if self.checkCollision():
            global IS_GAMEOVER
            IS_GAMEOVER = True;
            self.segments = self.segments[1:]
            return;
        if(self.segments[0].equals(apple.pos)):
            global SCORE
            global WAIT
            SCORE = SCORE + 1
            WAIT = 0.95*WAIT
            apple.move()
        else:
            self.segments = self.segments[:len(self.segments)-1]
    def checkCollision(self):
        hasCollided = False
        for segment in self.segments[1:]:
            hasCollided = hasCollided or segment.equals(self.segments[0])
        head = self.segments[0]
        if(head.x>WINDOWW/boxSize-2 or head.x<1 or head.y<1 or head.y>WINDOWH/boxSize-2):
            hasCollided = True
        return hasCollided

class Apple():
    def __init__(self,x,y):
        print(x)
        self.pos = Location(x,y)
    def move(self):
        self.pos = Location(random.randint(1, WINDOWW/boxSize-1)-1, random.randint(3, WINDOWH/boxSize)-2)
        
    def draw(self):
        pygame.draw.circle(DISPLAYSURF,(0,255,0),((self.pos.x*boxSize)+int(math.floor(boxSize/2)),(self.pos.y*boxSize)+int(math.floor(boxSize/2))),int(math.floor(boxSize/2)))

class Location():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def equals(self,loc):
        return self.x == loc.x and self.y == loc.y
            
def drawArena():
    DISPLAYSURF.fill((180,180,180))
    wall1 = pygame.Rect(0,0,boxSize,WINDOWH)
    pygame.draw.rect(DISPLAYSURF, (90,90,90), wall1)
    wall2 = pygame.Rect(WINDOWW-boxSize, 0, boxSize, WINDOWH)
    pygame.draw.rect(DISPLAYSURF, (90,90,90), wall2)
    wall3 = pygame.Rect(0,0,WINDOWW,boxSize)
    pygame.draw.rect(DISPLAYSURF, (90,90,90), wall3)
    wall4 = pygame.Rect(0,WINDOWH-boxSize,WINDOWW,boxSize)
    pygame.draw.rect(DISPLAYSURF, (90,90,90), wall4)

def drawScore():
    scoreObj = FONT_OBJ.render('Score: '+str(SCORE), True, (0,0,0))
    scoreRectObj = scoreObj.get_rect()
    scoreRectObj.left = boxSize
    scoreRectObj.top = boxSize*1
    speedObj = FONT_OBJ.render('Speed: '+str(math.floor((1000/WAIT)*10)/100), True, (0,0,0))
    speedRectObj = speedObj.get_rect()
    speedRectObj.left = boxSize
    speedRectObj.top = boxSize*3
    DISPLAYSURF.blit(scoreObj, scoreRectObj)
    DISPLAYSURF.blit(speedObj, speedRectObj)
    

def gameOver():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 60)
    gameOverObj = gameOverFont.render('Game Over', True, (0,0,0))
    gameOverRect = gameOverObj.get_rect()
    gameOverRect.center = (WINDOWW/2,WINDOWH/2)
    DISPLAYSURF.blit(gameOverObj, gameOverRect)
    

snake = Snake()
apple = Apple(5,7)
while True: # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() 
        elif event.type == KEYDOWN:
            if (event.key == K_LEFT or event.key == K_a) and snake.direction != RIGHT:
                snake.nextDirection = LEFT
            elif (event.key == K_RIGHT or event.key == K_d) and snake.direction != LEFT:
                snake.nextDirection = RIGHT
            elif (event.key == K_UP or event.key == K_w) and snake.direction != DOWN:
                snake.nextDirection = UP
            elif (event.key == K_DOWN or event.key == K_s) and snake.direction != UP:
                snake.nextDirection = DOWN
        
    drawArena()
    if IS_GAMEOVER:
        gameOver()
    else:
        snake.move()
    snake.draw()
    drawScore()
    apple.draw()
    pygame.display.update()
    fpsClock.tick(1000/WAIT)
        

