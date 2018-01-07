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
    pos_x, pos_y, player_name, world_grid = conn.root.start_game(player_name)
    dim = len(world_grid)
    win_dim_x = 2 * pict_size * dim
    win_dim_y = pict_size * dim
    pygame.init()
    window = pygame.display.set_mode((win_dim_x, win_dim_y))
    fond = pygame.Surface((2*pict_size * dim, pict_size * dim))
    fond.fill((255,255,255))
    pygame.display.set_caption('THE SR GAME')
    score = ""
    myfont = pygame.font.SysFont("Monospace", 14)
    # score_display = myfont.render(score, 1, (255, 0, 0))

    # pos_x, pos_y, player_name, world_grid = conn.root.init_world(player_name)
    world = World(dimensions=(dim, dim))
    world.set_world(world_grid)

    player = Player(pos_x, pos_y, player_name, conn, world)
    player.set_pos(pos_x, pos_y)

    best_player = ""
    score_tab = ""
    done = False  # Done is true when we close game
    first_game = True
    game_started = False  # game_started is true when
    while not done:
        # if (not game_started):
            # window.blit(myfont.render("Space to start the game", 1, (255, 0, 0)), (325, 2 * pict_size))
        # else:
        score_tab = conn.root.get_score_tab()
        window.blit(fond, (325, 0))
        y = 10
        for ligne in score_tab.splitlines():
            window.blit(myfont.render(ligne, 1, (255, 0, 0)), (325, y))
            y += pict_size

            #conn.root.generate_new_world()
            #conn.root.reset_score()
            #game_started = False
            #print("Welcome to a new game")
            #window.blit(pygame.Surface((2*pict_size * dim, pict_size * dim)), (325, 0))
            #if(player_init):
            #    best_player = conn.root.get_best_player()
            #    window.blit(myfont.render(best_player + " win last game!", 1, (255, 0, 0)), (325, 10))
            #window.blit(myfont.render("Space to start the game", 1, (255, 0, 0)), (325, 2 * pict_size))
            #conn.root.reset_score()
            #if(not game_started):
                #conn.root.generate_new_world()
                #conn.root.reset_score()
            #game_started = False
            #first_game = False


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
                        end, movable = conn.root.move(choice)
                        if movable:
                            print("You move to right")
                        else:
                            print("You can't move to right")
                    elif event.key == K_LEFT:
                        choice = 'left'
                        end, movable = conn.root.move(choice)
                        if movable:
                            print("You move to left")
                        else:
                            print("You can't move to left")
                    elif event.key == K_UP:
                        choice = 'top'
                        end, movable = conn.root.move(choice)
                        if movable:
                            print("You move to top")
                        else:
                            print("You can't move to top")
                    elif event.key == K_DOWN:
                        choice = 'bot'
                        end, movable = conn.root.move(choice)
                        if movable:
                            print("You move to bot")
                        else:
                            print("You can't move to bot")
                    #player.set_score(conn.root.get_score())
                #if end:
                #    best_player = conn.root.get_best_player()
                #    window.blit(fond, (325, 0))
                #    window.blit(myfont.render(best_player + " win last game!", 1, (255, 0, 0)), (325, 10))


        world.set_world(conn.root.get_world())

        world.display(window)

        # window.blit(score_display, (325, 10))
        pygame.display.flip()

