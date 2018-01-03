from random import choices, randint
import rpyc
from rpyc.utils.server import ThreadedServer  # or ForkingServer
from time import time


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
    _players = []

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
        self._world[y][x] = 1
        self._players.append({"player": self._conn, "coords": (x, y)})
        player_name = 'Player' + str(len(self._players) - 1)
        print('new player joined the game: ' + player_name)
        for player in [d['player'] for d in self._players]:
            player.root.notify_new_player(player_name)

    """
        called when a player is connected and want to spawn,
        so the server finds him a correct place and say him to redraw
    """

    def exposed_start_game(self):
        self._conn.root.draw(self._world)
        print("test")

    def on_disconnect(self):
        try:
            index = self._players.index(self._conn)  # O(size - index)
            del self._players[index]  # O(size - index)
            player_name = 'Player' + str(index)
            print('player left:', player_name)
            for player in [d['player'] for d in self._players]:
                player.root.notify_player_left(player_name)
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
