#!/usr/bin/python3

import sys
import pygame
from libs.GameView import *

if __name__ == '__main__':
    FPS = 60
    clock = pygame.time.Clock()
    
    # The view
    gameView = PongView()

    while True:
        # Controller
        #goUp = 0
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                gameView.exitGame()
                sys.exit()

        gameView.update()
        dt = clock.tick(FPS)