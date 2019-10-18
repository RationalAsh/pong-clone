import pygame
from pygame.locals import *

class PongView(object):
    """
    Class that sets up the game view.
    """
    def __init__(self):
        # Initialize pygame
        pygame.init()

        self.SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.BACKGROUND = (0, 0, 0)
        self.LINECOLOR = (255, 255, 255)
        self.CENTERLINECOLOR = (255, 255, 255, 128)
        self.FONTCOLOR = (245, 245, 245, 1)

        # Print the window size
        self.info = pygame.display.Info()
        self.width = self.info.current_w
        self.height = self.info.current_h
        self.bar_t = int(self.height*0.005)
        self.bat_length = int(self.height*0.05)
        self.bat_thickness = int(self.width*0.005)
        print(self.info.current_h, self.info.current_w)

        # Initialize fonts
        pygame.font.init()
        try:
            self.scoreFont = pygame.font.Font('assets/fonts/digital-7.regular.ttf', 150)
        except:
            self.scoreFont = pygame.font.Font(pygame.font.get_default_font(), 150)

    def update(self, gameStateDict=None):
        """
        Update the view with the current game state.
        """
        # Draw background.
        self.SCREEN.fill(self.BACKGROUND)

        # Draw the borders.
        border_rect = Rect(0, 0, self.width, self.height)
        pygame.draw.rect(self.SCREEN, self.LINECOLOR, 
                         border_rect, self.bar_t)

        # Draw the center line.
        pygame.draw.line(self.SCREEN, self.CENTERLINECOLOR,
                         (self.width//2, 0), (self.width//2, self.height),
                         self.bar_t)

        # Draw the scores for each player.
        player1_score = self.scoreFont.render('0', True, self.FONTCOLOR, self.BACKGROUND)
        player1_score_pos = player1_score.get_rect()
        player1_score_pos.center = (self.width*0.48 - player1_score_pos.width/2, 
                                    self.height*0.015 + player1_score_pos.height/2)
        player2_score = self.scoreFont.render('0', True, self.FONTCOLOR, self.BACKGROUND)
        player2_score_pos = player2_score.get_rect()
        player2_score_pos.center = (self.width*0.52 + player1_score_pos.width/2, 
                                    self.height*0.015 + player2_score_pos.height/2)
        
        self.SCREEN.blit(player1_score, player1_score_pos)
        self.SCREEN.blit(player2_score, player2_score_pos)

        # Draw the bats
        pygame.draw.line(self.SCREEN, self.LINECOLOR, 
                         (self.bar_t*1.8, 5), 
                         (self.bar_t*1.8, 5+self.bat_length),
                         self.bat_thickness)
        pygame.draw.line(self.SCREEN, self.LINECOLOR, 
                         (self.width-self.bar_t-self.bat_thickness/2, 5), 
                         (self.width-self.bar_t-self.bat_thickness/2, 5+self.bat_length),
                         self.bat_thickness)

        # Update
        pygame.display.update()

    def exitGame(self):
        pygame.quit()