import pygame
import random

class Ball(object):
    """
    Ball object.
    """
    def __init__(self, x, y, vx, vy):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(vx, vy)

    def reset(self, x, y, vx, vy):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(vx, vy)

    def step(self, dt):
        self.pos = self.pos + self.vel*dt


class Bat(object):
    """
    Bat Object
    """
    def __init__(self, x, y, length, thickness):
        self.rectangle = pygame.Rect(x, y, thickness, length)

class GameModel(object):
    def __init__(self, width, height):
        """
        Initialize game model.

        Parameters
        ----------
        width : int
            Width of the screen.
        height : int
            Height of the screen.
        """
        # Determine some display parameters
        self.border_t = height*0.005
        self.game_border = pygame.Rect(0, 0, width, height)
        self.ball_border = pygame.Rect(self.border_t, self.border_t,
                                       width-2*self.border_t,
                                       height-2*self.border_t)
        self.bat_thickness = width*0.005
        self.bat_length = height*0.05
        self.ball_radius = width*height*0.0000038
        self.font_size = 150
        self.width = width
        self.height = height

        # The ball
        starting_vel = random.choice([-1, 1])*width/5.5
        self.ball = Ball(width//2, height//2, starting_vel, 0)

        # The bats
        self.bat1 = Bat(self.border_t, height//2, self.bat_length,
                        self.bat_thickness)
        self.bat2 = Bat(width-self.border_t-self.bat_thickness, 
                        height//2, self.bat_length,
                        self.bat_thickness)

        # The scores
        self.score1 = 0
        self.score2 = 0

        # Events
        self.event = None
        self.EVENT_HIT = 1
        self.EVENT_MISS = 2

        # States
        self.STATE_PREGAME = 1
        self.STATE_PLAYING = 2
        self.STATE_POSTMISS = 3
        self.STATE_OVER = 4
        self.state = self.STATE_PREGAME

    def reset(self):
        # The ball
        starting_vel = random.choice([-1, 1])*self.width/5.5
        self.ball = Ball(self.width//2, self.height//2, starting_vel, 0)

        # The bats
        self.bat1 = Bat(self.border_t, self.height//2, self.bat_length,
                        self.bat_thickness)
        self.bat2 = Bat(self.width-self.border_t-self.bat_thickness, 
                        self.height//2, self.bat_length,
                        self.bat_thickness)

        # The scores
        self.score1 = 0
        self.score2 = 0

        # Event
        self.event = None
        # State
        self.state = self.STATE_PREGAME

    def step(self, p1y, p2y, dt):
        

