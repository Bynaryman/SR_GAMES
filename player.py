from common import *
import pygame
from pygame.locals import *

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


    def move(self, direction):
        print("ok")
        '''
        """

        :param direction:
        :return:
        """
        dim_x, dim_y = self.world.get_dimensions()

        if direction == 'right':
            if self.case_x < (dim_x - 1):
                # exemple d'un cas à traiter s'il y a un bombom
                # if self.world.get_world()[self.case_y][self.case_x + 1] != 2:
                self.case_x += 1
                self.x = self.case_x * pict_size

        if direction == 'left':
            if self.case_x > 0:
                # if self.world.get_world()[self.case_y][self.case_x - 1] != 2:
                self.case_x -= 1
                self.x = self.case_x * pict_size

        if direction == 'top':
            if self.case_y > 0:
                # if self.world.get_world()[self.case_y - 1][self.case_x] != 2:
                self.case_y -= 1
                self.y = self.case_y * pict_size

        if direction == 'bot':
            if self.case_y < (dim_y - 1):
                # if self.world.get_world()[self.case_y + 1][self.case_x] != 2:
                self.case_y += 1
                self.y = self.case_y * pict_size
    '''

    def display(self, window_ref):
        p = pygame.image.load(pict_player).convert_alpha()
        window_ref.blit(p, (self.x, self.y))


if __name__ == '__main__':

    """
        Simple main to test the class Player
        We need a world to pass it to the player (the player has to have a world)
        We need to create a window to pass it to the world
        Then we create a simple always loop waiting for application termination
        We always redraw all (world + player) @ 10FPS (theoric)
    """


    from world import World
    from pygame.locals import *
    from random import choices

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

        # we randomly move the player at each tick
        player.move(choices(['bot', 'top', 'right', 'left'], [1, 1, 1, 1])[0])

        world.display(window)
        player.display(window)
        pygame.display.flip()
