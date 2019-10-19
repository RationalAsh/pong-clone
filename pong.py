#!/usr/bin/python3

import sys
import pygame
from libs.GameView import *
from libs.bat import *
from libs.ball import *

if __name__ == '__main__':
    FPS = 60
    clock = pygame.time.Clock()
    
    # The view
    gameView = PongView()
    # Bats
    p1_bat = Bat(max_pos=gameView.height-gameView.bar_t-gameView.bat_length)
    p2_bat = Bat(max_pos=gameView.height-gameView.bar_t-gameView.bat_length)
    # Ball
    ball = Ball(bounding_box=gameView.get_ball_bb())
    # Scores
    p1_score = 0
    p2_score = 0

    while True:
        # Controller
        #goUp = 0
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                gameView.exitGame()
                sys.exit()
            elif (event.type == KEYDOWN and event.key == K_UP):
                p1_bat.move_up(10)
                p2_bat.move_up(10)
            elif (event.type == KEYDOWN and event.key == K_DOWN):
                p1_bat.move_down(10)
                p2_bat.move_down(10)

        mx, my = pygame.mouse.get_pos()
        p1_bat.set_pos(my)
        p2_bat.set_pos(my)
        #print(ball.x, ball.y)
        ball.update(b1_pos=(my, gameView.bat_length),
                    b2_pos=(my, gameView.bat_length),
                    dt=1.0/FPS)

        # Update the score
        if ball.ball_state == 0:
            # Score!
            if ball.x > gameView.width//2:
                p1_score += 1
            else:
                p2_score += 1
            ball.reset()
        
        gameStateDict = {'bat1': p1_bat.pos, 'bat2': p2_bat.pos,
                         'ball': (int(ball.x), int(ball.y)),
                         'p1_score': p1_score, 'p2_score': p2_score}

        gameView.update(gameStateDict=gameStateDict)
        dt = clock.tick(FPS)