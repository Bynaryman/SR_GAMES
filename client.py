from random import choices

import rpyc

from player import Player
from common import *
import pygame
from pygame.locals import *
from world import World


class GameClient(rpyc.Service):

    def on_connect(self):
        print('connecting...')

    def exposed_notify_new_player(self, player_name):
        print('new player joined the game', player_name)

    def exposed_notify_player_left(self, player_name):
        print('a player left the game', player_name)


if __name__ == '__main__':

    conn = rpyc.connect('127.0.0.1', 12345, service=GameClient)

    dim = 10
    win_dim_x = win_dim_y = pict_size * dim

    pygame.init()
    window = pygame.display.set_mode((win_dim_x, win_dim_y))
    pygame.display.set_caption('THE ST GAME')

    world = World(dimensions=(dim, dim))
    pos_x, pos_y = world.get_available_spawnable_pos()
    player = Player(pos_x, pos_y, 'blitzcrank', None, world)

    done = False

    while not done:

        pygame.time.Clock().tick(10)
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == KEYDOWN:
                # TODO aller dans menu si echap ?
                # if event.key == K_ESCAPE:
                if event.key == K_RIGHT:
                    choice = 'right'
                    if conn.root.move(choice):
                        player.move(choice)
                elif event.key == K_LEFT:
                    choice = 'left'
                    if conn.root.move(choice):
                        player.move(choice)
                elif event.key == K_UP:
                    choice = 'top'
                    if conn.root.move(choice):
                        player.move(choice)
                elif event.key == K_DOWN:
                    choice = 'bot'
                    if conn.root.move(choice):
                        player.move(choice)

        # we randomly move the player at each tick
        # choice = choices(['bot', 'top', 'right', 'left'], [1, 1, 1, 1])[0]


        world.display(window)
        player.display(window)
        pygame.display.flip()

