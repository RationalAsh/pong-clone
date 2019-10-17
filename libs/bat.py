import math

class Bat(object):
    def __init__(self, playernum=1):
        """
        Constructor.
        """
        self.playernum = playernum
        self.pos = 0

    def set_position(self, pos):
        self.pos = pos

    def move_up(self):
        pass

    def move_down(self):
        pass