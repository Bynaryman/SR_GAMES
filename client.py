from random import choices

import namesgenerator
import rpyc
from player import Player
from common import *
import pygame
from pygame.locals import *
from world import World
import argparse


class ArgumentParserError(Exception):
    pass


class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)


class GameClient(rpyc.Service):

    def on_connect(self):
        print('connecting...')

    def exposed_notify_new_player(self, player_name):
        print('new player joined the game', player_name)

    def exposed_notify_player_left(self, player_name):
        print('a player left the game', player_name)


if __name__ == '__main__':

    parser = ThrowingArgumentParser(description='the SR game client')
    parser.add_argument('-n', '--name', dest='name', metavar='[name]', required=False)

    player_name = ''
    try:
        args = parser.parse_args()
        if args.name is None:
            player_name = namesgenerator.get_random_name()
        else:
            player_name = args.name
    except ArgumentParserError:
        parser.print_usage()

    conn = rpyc.connect('127.0.0.1', 12345, service=GameClient)
    x, y, player_name, world_grid = conn.root.start_game(player_name)

    dim = len(world_grid)
    win_dim_x = win_dim_y = pict_size * dim

    pygame.init()
    window = pygame.display.set_mode((win_dim_x, win_dim_y))
    pygame.display.set_caption('THE SR GAME')

    world = World(dimensions=(dim, dim))
    world.set_world(world_grid)
    pos_x, pos_y = x, y
    player = Player(pos_x, pos_y, player_name, conn, world)

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

