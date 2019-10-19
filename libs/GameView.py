import pygame
from pygame.locals import *

class PongView(object):
    """
    Class that sets up the game view.
    """
    def __init__(self):
        pygame.mixer.pre_init(44100,-16,2, 128)
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

        # Initialize fonts
        pygame.font.init()
        try:
            self.scoreFont = pygame.font.Font('assets/fonts/digital-7.regular.ttf', 150)
        except:
            self.scoreFont = pygame.font.Font(pygame.font.get_default_font(), 150)

        # Initialize sounds
        pygame.mixer.init()
        self.hit_sound = pygame.mixer.Sound('assets/sounds/hit.wav')
        self.bounce_sound = pygame.mixer.Sound('assets/sounds/bounce.wav')
        self.miss_sound = pygame.mixer.Sound('assets/sounds/miss.wav')

    # def get_ball_bb(self):
    #     """
    #     Get the bounding box of the ball
    #     """
    #     left = self.bar_t + self.bat_thickness
    #     top = self.bar_t
    #     width = self.width - 2*(self.bar_t + self.bat_thickness)
    #     height = self.height - 2*self.bar_t
        
    #     return pygame.Rect(left, top, width, height)

    def update(self, gameModel):
        """
        Update the view with the current game state.
        """
        # Draw background.
        self.SCREEN.fill(self.BACKGROUND)

        # Draw the borders.
        border_rect = gameModel.game_border
        pygame.draw.rect(self.SCREEN, self.LINECOLOR, 
                         border_rect, int(gameModel.border_t))

        # pygame.draw.rect(self.SCREEN, self.LINECOLOR, 
        #                  self.get_ball_bb(), 1)

        # Draw the center line.
        pygame.draw.line(self.SCREEN, self.CENTERLINECOLOR,
                         (self.width//2, 0), (self.width//2, self.height),
                         int(gameModel.border_t))

        # Draw the scores for each player.
        player1_score = self.scoreFont.render(str(gameModel.score1), 
                                              True, self.FONTCOLOR,
                                              self.BACKGROUND)
        player1_score_pos = player1_score.get_rect()
        player1_score_pos.center = (self.width*0.48 - player1_score_pos.width/2, 
                                    self.height*0.015 + player1_score_pos.height/2)
        player2_score = self.scoreFont.render(str(gameModel.score2), 
                                              True, self.FONTCOLOR, 
                                              self.BACKGROUND)
        player2_score_pos = player2_score.get_rect()
        player2_score_pos.center = (self.width*0.52 + player1_score_pos.width/2, 
                                    self.height*0.015 + player2_score_pos.height/2)
        
        self.SCREEN.blit(player1_score, player1_score_pos)
        self.SCREEN.blit(player2_score, player2_score_pos)

        # Draw the bats
        pygame.draw.rect(self.SCREEN, self.LINECOLOR,
                         gameModel.bat1.rect)
        pygame.draw.rect(self.SCREEN, self.LINECOLOR,
                         gameModel.bat2.rect)
        # pygame.draw.line(self.SCREEN, self.LINECOLOR, 
        #                  (self.bar_t*1.8, self.bar_t + b1_pos), 
        #                  (self.bar_t*1.8, self.bar_t + b1_pos + self.bat_length),
        #                  self.bat_thickness)
        # pygame.draw.line(self.SCREEN, self.LINECOLOR, 
        #                  (self.width-self.bar_t-self.bat_thickness/2, self.bar_t + b2_pos), 
        #                  (self.width-self.bar_t-self.bat_thickness/2, self.bar_t + b2_pos + self.bat_length),
        #                  self.bat_thickness)

        # Draw the ball
        ball_pos = gameModel.ball.pos
        pygame.draw.circle(self.SCREEN, self.LINECOLOR,
                           (int(ball_pos.x), int(ball_pos.y)),
                           int(gameModel.ball_radius))

        # Indicate Pre-Game
        if gameModel.state == gameModel.STATE_PREGAME:
            pregame_text = self.scoreFont.render("Press any key to start.", 
                                                 True, self.FONTCOLOR,
                                                 self.BACKGROUND)
            pregame_text_pos = pregame_text.get_rect()
            pregame_text_pos.center = (self.width//2, self.height//2)
            self.SCREEN.blit(pregame_text, pregame_text_pos)

        # Indicate post game
        if gameModel.state == gameModel.STATE_OVER:
            if gameModel.score1 < gameModel.score2:
                winner = 2
            else:
                winner = 1
            pregame_text = self.scoreFont.render("GAME OVER. Player {} wins!".format(winner), 
                                                 True, self.FONTCOLOR,
                                                 self.BACKGROUND)
            pregame_text_pos = pregame_text.get_rect()
            pregame_text_pos.center = (self.width//2, self.height//2)
            self.SCREEN.blit(pregame_text, pregame_text_pos)

        # Indicate hit
        if gameModel.event == gameModel.EVENT_HIT:
            self.hit_sound.play()
        elif gameModel.event == gameModel.EVENT_WALLBOUNCE:
            self.bounce_sound.play()
        elif gameModel.event == gameModel.EVENT_MISS:
            self.miss_sound.play()

        # Update
        pygame.display.update()

    def exitGame(self):
        pygame.quit()