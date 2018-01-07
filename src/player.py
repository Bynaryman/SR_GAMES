import pygame
from common.common import *


class Player:
    """

    """
    def __init__(self, x, y, name, conn, world_ref):
        self.x = x * pict_size
        self.y = y * pict_size
        self.name = name
        self.score = 0
        self.conn = conn
        self.pict = pict_player
        self.case_x = x
        self.case_y = y
        self.world = world_ref

    def get_pos(self):
        return self.case_x, self.case_y

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score

    def get_name(self):
        return self.name

    def get_conn(self):
        return self.conn

    def __repr__(self):
        return "Player : " + self.name + ", Coords : (" + str(self.case_x) + "," + str(self.case_y) + "), Score : " \
               + str(self.score)


if __name__ == '__main__':

    """
        Simple main to test the class Player
        We need a world to pass it to the player (the player has to have a world)
        We need to create a window to pass it to the world
        Then we create a simple always loop waiting for application termination
        We always redraw all (world + player) @ 10FPS (theoric)
    """

    from src.world import World
    from pygame.locals import *

    dim = 10
    win_dim_x = win_dim_y = pict_size * dim

    pygame.init()
    window = pygame.display.set_mode((win_dim_x, win_dim_y))
    pygame.display.set_caption('test Player class')

    world = World(dimensions=(dim, dim))
    pos_x, pos_y = world.get_available_spawnable_pos()
    player = Player(pos_x, pos_y, 'blitzcrank', None, world)

    done = False

    while not done:

        pygame.time.Clock().tick(10)
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True

        world.display(window)
        pygame.display.flip()
