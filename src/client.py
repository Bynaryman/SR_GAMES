import namesgenerator
import rpyc
from src.player import Player
import pygame
from pygame.locals import *
from src.world import World
import argparse
from common.common import *


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

    def exposed_notify_end_game(self, list_winner, score):
        player_name = ""
        for winner in list_winner:
            player_name +=  winner + ", "
        print(player_name + " won last game with " + str(score) + " sweets!")
        print("Space bar or move to join the new game")


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
    if(conn.root.is_game_full()):
       print("Game is full")
    else:
        pos_x, pos_y, player_name, world_grid = conn.root.start_game(player_name)
        dim = len(world_grid)
        win_dim_x = 2 * pict_size * dim
        win_dim_y = pict_size * dim

        pygame.init()
        window = pygame.display.set_mode((win_dim_x, win_dim_y))
        fond = pygame.Surface((2*pict_size * dim, pict_size * dim))
        fond.fill((255,255,255))
        pygame.display.set_caption('THE SR GAME')
        myfont = pygame.font.SysFont("Monospace", 14)
        world = World(dimensions=(dim, dim))
        world.set_world(world_grid)

        done = False  # Done is true when we close game
        game_started = False  # game_started is true when
        while not done:

            window.blit(fond, (dim * pict_size + 5, 0))
            if (not game_started):
                window.blit(myfont.render("Space to start the game", 1, (255, 0, 0)), (dim * pict_size + 5, 10))

            score_tab = conn.root.get_score_tab()
            y = 10 + pict_size
            for ligne in score_tab.splitlines():
                window.blit(myfont.render(ligne, 1, (255, 0, 0)), (dim * pict_size + 5, y))
                y += pict_size/2

            #time.sleep(3) # Permet de tester la concurrence et ca marche
            pygame.time.Clock().tick(10)
            for event in pygame.event.get():
                if event.type == QUIT:
                    done = True
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        conn.root.start()
                        game_started = True
                    if game_started:
                        if event.key == K_RIGHT:
                            choice = 'right'
                            if not conn.root.move(choice):
                                print("You can't move to right")
                        elif event.key == K_LEFT:
                            choice = 'left'
                            if not conn.root.move(choice):
                                print("You can't move to left")
                        elif event.key == K_UP:
                            choice = 'top'
                            if not conn.root.move(choice):
                                print("You can't move to top")
                        elif event.key == K_DOWN:
                            choice = 'bot'
                            if not conn.root.move(choice):
                                print("You can't move to bot")


            world.set_world(conn.root.get_world())
            world.display(window)
            pygame.display.flip()

