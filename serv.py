from random import choices, randint
import rpyc
from rpyc.utils.server import ThreadedServer  # or ForkingServer
import namesgenerator
from player import Player
from world import World
from common import *

class GameServer(rpyc.Service):
    """

    Attributes:
        _world      A two dimension grid of int where : - 0 represents nothing (absence of all)
                                                        - 1 represents a player
                                                        - 2 represents a sweet
                    Example of a 4*4 world : [[0, 2, 0, 0],
                                              [0, 0, 0, 0],
                                              [0, 0, 1, 0],
                                              [0, 0, 0, 0]]

        _players   A one dimension array of dictionaries

                Example of the array at one moment :
                [ ... ]

    """

    """
    _world = [[choices([0, 2], [0.7, 0.3])[0] for _ in range(10)] for _ in range(10)]
    _players = []
    _names_pick = []
    """

    """
    def __init__(self, conn):
        super().__init__(conn)
        dim = 10
        world = World(dimensions=(dim, dim))
        self.names_pick = []
        self.players = []
        self.world = world
    """


    dim = 10
    world = World(dimensions=(dim, dim))
    names_pick = []
    players = []
    world = world

    def on_connect(self):
        print('someone connected')

    def exposed_start_game(self, name):
        x, y = self.world.get_available_spawnable_pos()
        if name in self.names_pick:
            name += ' :)'
        player = Player(x, y, name, self._conn, self.world)
        self.players.append(player)
        print('new player joined the game: ' + name)
        for player in self.players:
            player.get_conn().root.notify_new_player(name)
        return x, y, name, self.world.get_world()

    def on_disconnect(self):
        for i, player in enumerate(self.players):
            if player.get_conn() == self._conn:
                player_name = player.get_name()
                x, y = player.get_pos()
                print('player left:', player_name, x, y)
                self.world.get_world()[x][y] = 0
                print(self.players)
                del self.players[i]
                print(self.players)
                for playerToNotify in self.players:
                    print('here')
                    playerToNotify.get_conn().root.notify_player_left(player_name)

    def exposed_get_players(self):
        return self._players

    def exposed_move(self, direction):
        is_allowed = False
        for i, player in enumerate(self.players):
            if player.get_conn() == self._conn:
                dim_x, dim_y = self.world.get_dimensions()

                player_name = player.get_name()
                print(player_name, 'wants to move to the', direction)
                # TODO : gerer bombons et score ici
                if direction == 'right':
                    if player.case_x < (dim_x - 1):
                        if self.world.get_world()[player.case_y][player.case_x + 1] != 1:
                            player.case_x += 1
                            player.x = player.case_x * pict_size # useless pour le server de savoir où il est en pixel ...
                            is_allowed = True
                if direction == 'left':
                    if player.case_x > 0:
                        if self.world.get_world()[player.case_y][player.case_x - 1] != 1:
                            player.case_x -= 1
                            player.x = player.case_x * pict_size
                            is_allowed = True
                if direction == 'top':
                    if player.case_y > 0:
                        if self.world.get_world()[player.case_y - 1][player.case_x] != 1:
                            player.case_y -= 1
                            player.y = player.case_y * pict_size
                            is_allowed = True
                if direction == 'bot':
                    if player.case_y < (dim_y - 1):
                        if self.world.get_world()[player.case_y + 1][player.case_x] != 1:
                            player.case_y += 1
                            player.y = player.case_y * pict_size
                            is_allowed = True
                return is_allowed

    def find_correct_place_to_spawn(self):
        dim_x, dim_y = len(self._world[0]), len(self._world)
        rand_x, rand_y = randint(0, dim_x - 1), randint(0, dim_y - 1)
        while self._world[rand_x][rand_y] != 0:
            rand_x, rand_y = randint(0, dim_x - 1), randint(0, dim_y - 1)
        return rand_x, rand_y


if __name__ == '__main__':
    """
        note: we can chose ThreadedServer, ForkingServer or even ThreadedPoolServer
        depending on the OS. Forking only works with UNIX based OS
    """

    server = ThreadedServer(GameServer, port=12345)
    server.start()
