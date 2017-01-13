import pygame
from pygame import Rect
from pygame.locals import *
import random

pygame.init()
fpsClock = pygame.time.Clock()

screen = pygame.display.set_mode((640,480))
pygame.display.set_caption('Pong')

black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)

font = pygame.font.Font("bit5x3.ttf",80)

#game variable
playerPaddle = Rect((20,480/2-20),(8,28))
aiPaddle = Rect((620,480/2-20),(8,28))
ball = Rect((640/2+20,480/2),(10,10))

maxSpeed = 10

player_a = 3
player_speed = 0

ai_v = 3
ai_speed = 0

playerScore = 0
aiScore = 0

speeds_y = [-6,-5,-4,4,5,6]
ball_speed_y = speeds_y[random.randint(0,5)];
speeds_x = [-6,6]
ball_speed_x = speeds_x[random.randint(0,1)];

#allows for holding of key
pygame.key.set_repeat(1,0)

#this is the game loop
while True:

    isPressed = False

    #player input
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

        if event.type == KEYDOWN:
            #press key
            if event.key == K_UP:
                isPressed = True
                if player_speed > -maxSpeed:
                    player_speed -= player_a

            if event.key == K_DOWN:
                isPressed = True
                if player_speed < maxSpeed:
                    player_speed += player_a

        if event.type == MOUSEBUTTONDOWN:
            #press key
            if event.button == 4:
                isPressed = True
                if player_speed > -maxSpeed:
                    player_speed -= player_a*3

            if event.button == 5:
                isPressed = True
                if player_speed < maxSpeed:
                    player_speed += player_a*3



    if not isPressed:
        if player_speed>0:
            player_speed -= player_a
        elif player_speed<0:
            player_speed += player_a

    #pure-AI input
    #if ball.x > 640/2:
    if ball.y > aiPaddle.centery:
        if ai_speed < maxSpeed:
                ai_speed += player_a
    elif ball.y < aiPaddle.centery:
        if ai_speed > -maxSpeed:
            ai_speed -= player_a
    else:
        if ai_speed>0:
            ai_speed -= player_a
        elif ai_speed<0:
            ai_speed += player_a

    #update
    playerPaddle.move_ip(0,player_speed)
    aiPaddle.move_ip(0,ai_speed)
    ball.move_ip(ball_speed_x,ball_speed_y)

    #collisions
    if playerPaddle.y <0:
        playerPaddle.y = 0
        player_speed = 0

    elif playerPaddle.bottom > 480:
        playerPaddle.bottom = 480
        player_speed = 0

    if aiPaddle.y <0:
        aiPaddle.y = 0
        ai_speed = 0

    elif aiPaddle.bottom > 480:
        aiPaddle.bottom = 480
        ai_speed = 0

    if playerPaddle.colliderect(ball):
        ball_speed_x = -ball_speed_x
        if player_speed == 0:
            ball_speed_y = ball_speed_y/abs(ball_speed_y)
        else:
            ball_speed_y = player_speed

        ball.left = playerPaddle.right +1


    elif aiPaddle.colliderect(ball):
        ball_speed_x = -ball_speed_x

        #prevent
        if ai_speed == 0:
            ball_speed_y = ball_speed_y/abs(ball_speed_y)
        else:
            ball_speed_y = ai_speed

        ball.right = aiPaddle.x -1



    if ball.y <= 0:
        ball.y = 0
        ball_speed_y = -ball_speed_y

    elif ball.y+10 >= 480:
        ball.y = 480-10
        ball_speed_y = -ball_speed_y

    if ball.x < 0 or ball.x > 640:
        if ball.x<0:
            aiScore += 1
        else:
            playerScore += 1
        ball_speed_x = speeds_x[random.randint(0,1)];
        ball_speed_y = speeds_y[random.randint(0,5)];
        ball.x = 640/2
        ball.y = 480/2





    #draw
    screen.fill(black)
    pygame.draw.rect(screen, white,playerPaddle)
    pygame.draw.rect(screen, white,aiPaddle)
    pygame.draw.rect(screen, white,ball)
    playerF = font.render(str(playerScore), True, white)
    aiF = font.render(str(aiScore), True, white)
    screen.blit(playerF,(200,25))
    screen.blit(aiF,(400,25))

    for i in range(30):
        pygame.draw.line(screen, white, (320,i*20), (320,i*20+10),5)

    pygame.display.update()
    fpsClock.tick(60)
