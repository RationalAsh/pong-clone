import math

class Bat(object):
    def __init__(self, starting_pos=0.0, min_pos=0.0, max_pos=1080):
        """
        Constructor.
        """
        self.pos = starting_pos
        self.min_pos = min_pos
        self.max_pos = max_pos

    def set_pos(self, pos):
        self.pos = pos
        
        if self.pos > self.max_pos:
            self.pos = self.max_pos
        elif self.pos < self.min_pos:
            self.pos = self.min_pos

    def move_down(self, delta=0.0):
        self.pos += delta

        if self.pos > self.max_pos:
            self.pos = self.max_pos
        elif self.pos < self.min_pos:
            self.pos = self.min_pos

    def move_up(self, delta=0.0):
        self.pos -= delta

        if self.pos > self.max_pos:
            self.pos = self.max_pos
        elif self.pos < self.min_pos:
            self.pos = self.min_pos