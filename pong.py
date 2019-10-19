#!/usr/bin/python3

import sys
import pygame
from libs.GameView import *
from libs.GameModel import *

if __name__ == '__main__':
    FPS = 100
    clock = pygame.time.Clock()
    
    # The view
    gameView = PongView()
    # The model
    gameModel = GameModel(gameView.width, gameView.height)

    while True:
        # Controller
        #goUp = 0
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                gameView.exitGame()
                sys.exit()
            elif (event.type == KEYDOWN and event.key == K_UP):
                gameModel.state = gameModel.STATE_PLAYING
            elif (event.type == KEYDOWN and event.key == K_DOWN):
                pass

        mx, my = pygame.mouse.get_pos()

        gameModel.step(my, my, 1.0/FPS)

        gameView.update(gameModel)
        dt = clock.tick(FPS)