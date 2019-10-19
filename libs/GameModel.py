import pygame
import random
import math

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
        self.rect = pygame.Rect(x, y, thickness, length)

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
        self.min_vel = abs(starting_vel)
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
        self.EVENT_WALLBOUNCE = 3

        # States
        self.STATE_PREGAME = 1
        self.STATE_PLAYING = 2
        self.STATE_POSTMISS = 3
        self.STATE_OVER = 4
        self.state = self.STATE_PREGAME

    def reset_positions(self):
        # The ball
        starting_vel = random.choice([-1, 1])*self.width/5.5
        self.ball = Ball(self.width//2, self.height//2, starting_vel, 0)

        # The bats
        self.bat1 = Bat(self.border_t, self.height//2, self.bat_length,
                        self.bat_thickness)
        self.bat2 = Bat(self.width-self.border_t-self.bat_thickness, 
                        self.height//2, self.bat_length,
                        self.bat_thickness)

        # Event
        self.event = None
        # State
        self.state = self.STATE_PREGAME

    def reset_ball(self):
        starting_vel = random.choice([-1, 1])*self.width/5.5
        self.ball = Ball(self.width//2, self.height//2, starting_vel, 0)


    def reset_scores(self):
        self.score1 = 0
        self.score2 = 0

    def check_collisions(self):
        hit_pos = -1
        # Check for collision or point
        if self.ball.pos.x <= self.ball_border.left + self.ball_radius:
            if (self.ball.pos.y >= self.bat1.rect.top - self.ball_radius) and\
                (self.ball.pos.y <= self.bat1.rect.bottom + self.ball_radius):
                self.event = self.EVENT_HIT
                hit_pos = (self.bat1.rect.bottom - self.ball.pos.y)/self.bat1.rect.h
            else:
                self.event = self.EVENT_MISS
        elif self.ball.pos.x >= self.ball_border.right - self.ball_radius:
            if (self.ball.pos.y >= self.bat2.rect.top - self.ball_radius) and\
                (self.ball.pos.y <= self.bat2.rect.bottom + self.ball_radius):
                self.event = self.EVENT_HIT
                hit_pos = (self.bat1.rect.bottom - self.ball.pos.y)/self.bat1.rect.h
            else:
                self.event = self.EVENT_MISS

        if (self.ball.pos.y >= self.ball_border.bottom - self.ball_radius) or\
            (self.ball.pos.y <= self.ball_border.top + self.ball_radius):
            #self.ball.vel.y = -self.ball.vel.y
            self.event = self.EVENT_WALLBOUNCE

        return hit_pos

    @staticmethod
    def get_bounce_vel(hit_pos, min_vel):
        """
        Compute the bounce velocity

        Parameters
        ----------
        current_vel : (vx, vy)
            Current velocity
        hit_pos : float
            The place the ball hit the bat (as a percentage of its length)

        Returns
        -------
        bounce_vel : (vx_new, vy_new)
            The new velocities
        """
        sf = abs(hit_pos - 0.5)**2
        new_speed = 2*sf*2.0*min_vel + min_vel
        new_angle = 2*(0.5 - hit_pos)*(math.pi/3)

        return (new_speed*math.cos(new_angle), new_speed*math.sin(new_angle))

    def step(self, p1y, p2y, dt):
        # Clear event flags
        self.event = None

        if self.state == self.STATE_PLAYING:
            # Adjust the position of the bats from controller input
            self.bat1.rect.centery = p1y
            self.bat2.rect.centery = p2y

            # Update the position of the ballGameModel.get_bounce_vel(hit_pos, self.min_vel)
            self.ball.step(dt)

            # Check for collision or point
            hit_pos = self.check_collisions()

            if self.event == None:
                pass
            elif self.event == self.EVENT_HIT:
                vx, vy = GameModel.get_bounce_vel(hit_pos, self.min_vel)
                print("New speed is {}, {}".format(vx, vy))
                if self.ball.pos.x > self.width//2:
                    self.ball.vel = pygame.Vector2(-vx, vy)
                    self.ball.pos.x = self.ball_border.right - self.ball_radius*1.01
                    print("Player 2 hits ball at {}.".format(hit_pos))
                else:
                    self.ball.vel = pygame.Vector2(vx, vy)
                    self.ball.pos.x = self.ball_border.left + self.ball_radius*1.05
                    print("Player 1 hits ball at {}.".format(hit_pos))
                
            elif self.event == self.EVENT_MISS:
                self.state = self.STATE_POSTMISS
                print("Player {} misses ball. Score!")
            elif self.event == self.EVENT_WALLBOUNCE:
                print("Ball bounces off wall.")
                self.ball.vel.y = -self.ball.vel.y
                # if self.ball.pos.y > self.height//2:
                #     self.ball.pos.y = self.ball_border.bottom - 1
                # else:
                #     self.ball.pos.y = self.ball_border.top + 1
        elif self.state == self.STATE_PREGAME:
            pass
        elif self.state == self.STATE_POSTMISS:
            if self.ball.pos.x > self.width//2:
                self.score1 += 1
            else:
                self.score2 += 1
            #self.reset_positions()
            self.reset_ball()

            if self.score1 == 11 or self.score2 == 11:
                self.state = self.STATE_OVER
            else:
                self.state = self.STATE_PLAYING
        elif self.state == self.STATE_OVER:
            pass


