from random import choices, randint
import pygame
from pygame.locals import *
from common import *


class World:
    """
        A class allowing a representation of a 2D world
    """

    def __init__(self, probability_sweet=0.3, dimensions=(10, 10)):
        self.dim_x, self.dim_y = dimensions
        self.world = [[choices([0, 2], [1 - probability_sweet, probability_sweet])[0] for _ in range(self.dim_x)]
                      for _ in range(self.dim_y)]

    def display(self, window_ref):
        """
        blit the different tiles of world into a window
        :param {pygame.display} window_ref: a window where the world will be displayed
        """

        grass = pygame.image.load(pict_grass).convert()
        sweet = pygame.image.load(pict_sweet).convert_alpha()

        for i, row in enumerate(self.world):
            for j, box in enumerate(row):
                x = i * pict_size
                y = j * pict_size
                window_ref.blit(grass, (x, y))
                if box == 2:  # 2 = sweet
                    window_ref.blit(sweet, (x, y))

    def get_world(self):
        return self.world

    def get_dimensions(self):
        return self.dim_x, self.dim_y

    def get_available_spawnable_pos(self):
        dim_x, dim_y = len(self.world[0]), len(self.world)
        rand_x, rand_y = randint(0, dim_x - 1), randint(0, dim_y - 1)
        while self.world[rand_x][rand_y] != 0:
            rand_y, rand_y = randint(0, dim_x - 1), randint(0, dim_y - 1)
        return rand_x, rand_y


if __name__ == '__main__':

    """
        Simple main to test the class World
        We need to create a window to pass it to the world
        Then we create a simple always loop waiting for application termination
        We always redraw the world @ 30FPS (theoric)
    """

    dim = 10
    win_dim_x = win_dim_y = pict_size * dim

    pygame.init()
    window = pygame.display.set_mode((win_dim_x, win_dim_y))
    pygame.display.set_caption('test World class')

    background = pict_background
    world = World(dimensions=(dim, dim))

    done = False

    while not done:
        pygame.time.Clock().tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
        world.display(window)
        pygame.display.flip()
