import pygame
import sys
import random
import copy
  
pygame.init()

tileSize = 30
boardWidth = 20

cells = [[i, j] for i in range(boardWidth) for j in range(boardWidth)]

red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)

foodPosX = 2
foodPosY = 2

foodCoordsX = tileSize*foodPosX
foodCoordsY = tileSize*foodPosY

food = pygame.Rect(foodCoordsX, foodCoordsY, tileSize, tileSize)

snakeMovementX = 1
SnakeMovementY = 0

snake = [[5,2],[4,2],[3,2]]

timeSinceSnakeMove = 0
clock = pygame.time.Clock()

screen = pygame.display.set_mode((tileSize*boardWidth, tileSize*boardWidth))
pygame.display.set_caption("Snake Game")
my_font = pygame.font.SysFont("monospace", 70)

pygame.display.update()

def move(snake, snakeMovementX, SnakeMovementY, foodPosX, foodPosY):
    snakeBuffer = copy.deepcopy(snake)
    snakeLength = len(snakeBuffer)
    foodStatus = False

    for cell in range(snakeLength):
        if cell != 0:
            snakeBuffer[cell] = snake[cell-1]

    snakeBuffer[0][0] += snakeMovementX
    snakeBuffer[0][1] += SnakeMovementY
    
    if snakeBuffer[0][0] == foodPosX and snakeBuffer[0][1] == foodPosY:
        foodStatus = True
        snakeBuffer.append(snake[-1])

    return snakeBuffer, foodStatus

foodStatus = False
exit = False
buffer = 5

while exit == False:

    dt = clock.tick()
    timeSinceSnakeMove += dt
    pygame.draw.rect(screen, red, food)
    if timeSinceSnakeMove > 200:

        screen.fill(black)
        moveRet = move(snake, snakeMovementX, SnakeMovementY, foodPosX, foodPosY)
        snake = moveRet[0]
        for i in snake:
            if snake.count(i) > 1 or i[0] >= boardWidth or i[1] >= boardWidth or i[0] < 0 or i[1] < 0:
                exit = True
          
        for index, cell in enumerate(snake):
            blockCoordsX = tileSize*cell[0]
            blockCoordsY = tileSize*cell[1]
            if index == 0:
                if SnakeMovementY == -1:
                    triangle_points = [(int(blockCoordsX) + buffer / 2, int(blockCoordsY) + tileSize - buffer), (int(blockCoordsX-1)+ tileSize - buffer/2, int(blockCoordsY) + tileSize - buffer), (int(blockCoordsX + tileSize / 2), int(blockCoordsY) + buffer / 2)]
                if SnakeMovementY == 1:
                    triangle_points = [(int(blockCoordsX) + buffer / 2, int(blockCoordsY) + buffer / 2), (int(blockCoordsX-1)+ tileSize - buffer / 2, int(blockCoordsY) + buffer / 2), (int(blockCoordsX + tileSize / 2), int(blockCoordsY) + tileSize - buffer / 2)]
                if snakeMovementX == -1:
                    triangle_points = [(int(blockCoordsX) + tileSize - buffer, int(blockCoordsY) + buffer / 2), (int(blockCoordsX) + tileSize - buffer, int(blockCoordsY)+tileSize-1-buffer/2), (int(blockCoordsX), int(blockCoordsY) + tileSize / 2)]
                if snakeMovementX == 1:
                    triangle_points = [(int(blockCoordsX) + buffer / 2, int(blockCoordsY) + buffer / 2), (int(blockCoordsX-1) + buffer / 2, int(blockCoordsY)+tileSize-1-buffer/2), (int(blockCoordsX) + tileSize - buffer / 2, int(blockCoordsY) + tileSize / 2)]
                pygame.draw.polygon(screen, green, triangle_points)
            else:
                block = pygame.Rect(blockCoordsX+buffer/2, blockCoordsY+buffer/2, tileSize-buffer, tileSize-buffer)
                pygame.draw.rect(screen, green, block)

        if moveRet[1] == True:
            freeCells = [i for i in cells if i not in snake]
            chosenCell = random.choice(freeCells)
            foodPosX = chosenCell[0]
            foodPosY = chosenCell[1]
            foodCoordsX = tileSize*foodPosX
            foodCoordsY = tileSize*foodPosY
            food = pygame.Rect(foodCoordsX, foodCoordsY, tileSize, tileSize)

        pygame.draw.rect(screen, red, food)
        pygame.display.update()
        timeSinceSnakeMove = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                SnakeMovementY = -1
                snakeMovementX = 0
            elif event.key == pygame.K_DOWN:
                SnakeMovementY = 1
                snakeMovementX = 0
            elif event.key == pygame.K_LEFT:
                snakeMovementX = -1
                SnakeMovementY = 0
            elif event.key == pygame.K_RIGHT:
                snakeMovementX = 1
                SnakeMovementY = 0


    while exit == True:
        label = my_font.render("Game Over", 1, white)
        label_rect = label.get_rect()
        label_rect.center = (boardWidth*tileSize/2, boardWidth+50)
        label2 = my_font.render("Length:" + str(len(snake)), 1, white)
        label2_rect = label2.get_rect()
        label2_rect.center = (boardWidth*tileSize/2, boardWidth + 140)
        screen.blit(label, label_rect)
        screen.blit(label2, label2_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    snakeMovementX = 1
                    SnakeMovementY = 0
                    snake = [[5,2],[4,2],[3,2]]
                    exit = False