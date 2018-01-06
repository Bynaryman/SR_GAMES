from random import choices

import namesgenerator
import rpyc
from player import Player
from common import *
import pygame
from pygame.locals import *
from world import World
import argparse
import time


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
    world_grid = conn.root.get_world()
    dim = len(world_grid)
    win_dim_x = pict_size * dim
    win_dim_y = pict_size * dim + 2*pict_size
    pygame.init()
    window = pygame.display.set_mode((win_dim_x, win_dim_y))
    pygame.display.set_caption('THE SR GAME')
    score = 0
    myfont = pygame.font.SysFont("Monospace", 24)
    score_display = myfont.render("You collected " + str(score) + " sweets", 1, (255, 0, 0))


    world = World(dimensions=(dim, dim))
    world.set_world(world_grid)

    done = False
    player_init = False
    game_started = False
    while not done:
        if (conn.root.is_end() or not player_init ):
            print("Welcome to a new game")
            print("Space to start the game")
            game_started = False
            pos_x, pos_y, player_name, world_grid = conn.root.init_world(player_name)
            player = Player(pos_x, pos_y, player_name, conn, world)
            player.set_pos(pos_x, pos_y)
            player_init = True
        if (game_started):
            best_player, best_score = conn.root.get_best_player()
            print("You collected " + str(player.get_score()) + " sweets.")
            if best_player == player.get_name():
                score = player.get_score()
                score_display = myfont.render("You collected " + str(score) + " sweets", 1, (255, 0, 0))
                print("Best player : It's you with " + str(player.get_score()) + " sweets!")
            else:
                print("Best player : " + best_player + " with " + str(best_score) + " sweets!")

        #time.sleep(3) # Permet de tester la concurrence et ca marche
        pygame.time.Clock().tick(10)
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == KEYDOWN:
                # TODO aller dans menu si echap ?
                # if event.key == K_ESCAPE:
                if event.key == K_SPACE:
                    conn.root.start()
                    game_started = True
                if game_started:
                    if event.key == K_RIGHT:
                        choice = 'right'
                        if conn.root.move(choice):
                            print("You move to right")
                        else:
                            print("You can't move to right")
                    elif event.key == K_LEFT:
                        choice = 'left'
                        if conn.root.move(choice):
                            print("You move to left")
                        else:
                            print("You can't move to left")
                    elif event.key == K_UP:
                        choice = 'top'
                        if conn.root.move(choice):
                            print("You move to top")
                        else:
                            print("You can't move to top")
                    elif event.key == K_DOWN:
                        choice = 'bot'
                        if conn.root.move(choice):
                            print("You move to bot")
                        else:
                            print("You can't move to bot")

                    player.set_score(conn.root.get_score())

        world.set_world(conn.root.get_world())

        # we randomly move the player at each tick
        # choice = choices(['bot', 'top', 'right', 'left'], [1, 1, 1, 1])[0]


        world.display(window)
        window.blit(score_display, (10, 325))
        #player.display(window)
        pygame.display.flip()

