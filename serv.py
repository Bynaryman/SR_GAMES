from random import choices, randint
import rpyc
from rpyc.utils.server import ThreadedServer  # or ForkingServer
import namesgenerator
from time import time
from Player import Player


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
                [{player: conn1, coords:(1, 2)},
                 {player: conn2, coords:(3, 2)}]

    """

    _world = [[choices([0, 2], [0.7, 0.3])[0] for _ in range(10)] for _ in range(10)]
    _players = {}

    """
        TODO
    """

    def __repr__(self):
        print('players: ', self._players, '\n')
        print('actual representation of world:\n')
        tmp = ''
        for i in self._world:
            tmp += ','.join(str(x) for x in i) + '\n'
        return tmp

    def on_connect(self):
        x, y = self.find_correct_place_to_spawn()
        self._world[x][y] = 1
        player_name = "P1"
        player = Player(x, y, player_name)
        print(self._conn.root.name)
        self._players[self._conn] = player
        print('new player joined the game: ' + player_name)
        for player in self._players.keys():
            player.notify_new_player(player_name)
            player.draw(self._world)

    """
        called when a player is connected and want to spawn,
        so the server finds him a correct place and say him to redraw
    """

    def exposed_start_game(self):
        self._conn.root.draw(self._world)

    def on_disconnect(self):
        try:
            player = self._players[self._conn.root]
            player_name = player.getName()
            x, y = player.getPos()
            self._world[x][y] = 0
            del self._players[self._conn]
            print(player_name, x, y)
            print('player left:', player_name)
            for player in self._players.keys():
                print(player)
                player.notify_player_left(player_name)
                player.draw(self._world)
        except ValueError:
            print('no such player')

    def exposed_get_players(self):
        return self._players

    def find_correct_place_to_spawn(self):
        dimX, dimY = len(self._world[0]), len(self._world)
        randX, randY = randint(0, dimX - 1), randint(0, dimY - 1)
        while self._world[randY][randX] != 0:
            randX, randY = randint(0, dimX - 1), randint(0, dimY - 1)
        return randX, randY


if __name__ == '__main__':
    """
        note: we can chose ThreadedServer, ForkingServer or even ThreadedPoolServer
        depending on the OS. Forking only works with UNIX based OS
    """

    server = ThreadedServer(GameServer, port=12345)
    server.start()
