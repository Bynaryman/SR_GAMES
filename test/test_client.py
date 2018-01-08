import unittest
from src.world import World
from pygame.locals import *
from common.common import *
import pygame
import rpyc
from random import choices


pygame.init()
window = pygame.display.set_mode((2 * 32 * 10, 32*10))

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

class TestGameClient(unittest.TestCase):

    def test_monkey(self):
        conn = rpyc.connect('127.0.0.1', 12344,service=GameClient)
        pos_x, pos_y, player_name, world_grid = conn.root.start_game("monkey")
        dim = len(world_grid)
        win_dim_x = 2 * pict_size * dim
        win_dim_y = pict_size * dim

        fond = pygame.Surface((2 * pict_size * dim, pict_size * dim))
        fond.fill((255, 255, 255))
        pygame.display.set_caption('THE SR GAME')
        myfont = pygame.font.SysFont("Monospace", 14)
        world = World(dimensions=(dim, dim))
        world.set_world(world_grid)
        # we randomly move the player at each tick
        done = False
        while not done:

            window.blit(fond, (dim * pict_size + 5, 0))
            score_tab = conn.root.get_score_tab()
            y = 10 + pict_size
            for ligne in score_tab.splitlines():
                window.blit(myfont.render(ligne, 1, (255, 0, 0)), (dim * pict_size + 5, y))
                y += pict_size / 2

            # time.sleep(3) # Permet de tester la concurrence et ca marche
            pygame.time.Clock().tick(10)
            choice = choices(['bot', 'top', 'right', 'left'], [1, 1, 1, 1])[0]
            print(conn.root.move(choice))

            world.set_world(conn.root.get_world())
            world.display(window)
            pygame.display.flip()


if __name__ == '__main__':
    unittest.main()