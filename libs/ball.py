import pygame
import math

class Ball(object):
    """
    The ball object
    """
    def __init__(self, starting_pos = (50, 50), bounding_box=(0, 0, 1970, 1070),
                 ball_vel=(300.0, -200.0), ball_radius=5, min_vel=300.0):
        """
        Constructor.

        Parameters
        -----------
        starting_pos : tuple
            (x, y) - the starting position of the ball.
        bounding_box : tuple
            (x, y, w, h) - The bounding rectangle inside which the ball must
            remain 
        ball_vel : tuple
            (vx, vy) - The ball velocity in the x and y directions.
        min_vel : float
            The minimum velocity of the ball
        """
        self.x, self.y = starting_pos
        left, top, width, height = bounding_box
        self.bounding_box = pygame.Rect(left+ball_radius, 
                                        top + ball_radius,
                                        width - 2*ball_radius, 
                                        height - 2*ball_radius)
        self.vx, self.vy = ball_vel
        self.ball_radius = ball_radius
        self.min_vel = min_vel
        self.ball_state = 1

    def reset(self, starting_pos=(50, 50), ball_vel=(300.0, 0.0),
              min_vel=300.0):
        """
        Reset the ball.
        """
        self.x, self.y = starting_pos
        self.vx, self.vy = ball_vel
        self.min_vel = min_vel
        self.ball_state = 1


    def get_bounce_vel(self, hit_pos):
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
        sf = abs(hit_pos - 0.5)
        new_speed = 3*sf*2.0*self.min_vel + self.min_vel
        new_angle = (hit_pos - 0.5)*(math.pi/3)

        return (new_speed*math.cos(new_angle), new_speed*math.sin(new_angle))

    def update(self, b1_pos=(0, 30), b2_pos=(1980, 30), dt=0.01):
        """
        Update the position of the ball.

        Parameters
        -----------
        b1_pos : tuple
            (y, width) - The position of player 1's bat.
        b2_pos : tuple
            (y, width) - The position of player 2's bat.
        dt : float
            The delta t since the last update.
        """
        if self.ball_state == 1:
            #Check for collisions.
            if (self.x <= self.bounding_box.left):
                if (self.y >= b1_pos[0]) and (self.y <= b1_pos[0] + b1_pos[1]):
                    hit_pos = (self.y - b1_pos[0])/b1_pos[1]
                    self.vx, self.vy = self.get_bounce_vel(hit_pos)
                    self.bounding_box.left + 1
                    print(hit_pos)
                    print(self.vx, self.vy)
                else:
                    #self.vx = 0
                    #self.vy = 0
                    self.ball_state = 0
            elif (self.x >= self.bounding_box.right):
                if (self.y >= b2_pos[0]) and (self.y <= b2_pos[0] + b2_pos[1]):
                    hit_pos = (self.y - b2_pos[0])/b2_pos[1]
                    self.vx, self.vy = self.get_bounce_vel(hit_pos)
                    self.vx = -self.vx
                    # self.vy = -self.vy
                    self.x = self.bounding_box.right-1
                    print(hit_pos)
                    print(self.vx, self.vy)
                else:
                    #self.vy = 0
                    #self.vx = 0
                    self.ball_state = 0
            elif (self.y >= self.bounding_box.bottom) or (self.y <= self.bounding_box.top):
                self.vy = -self.vy
                self.vx = self.vx*1.1

        # Update the position of the ball
        self.x += self.vx*dt
        self.y += self.vy*dt


    