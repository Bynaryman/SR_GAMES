from random import choices
import rpyc
from rpyc.utils.server import ThreadedServer  # or ForkingServer


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
        _sweet_probability
        _players

    """

    _world = []
    _players = []
    _sweet_probability = 0.3
    _dim = (10, 10)

    def __init__(self, dim):
        self._conn = None
        self._dim = dim
        super().__init__(self)
        self._init_world()

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
        self._players.append(self._conn)
        print('new player:', self._conn)

    def on_disconnect(self):
        self._players.remove(self._conn)
        print('player left:', self._conn)

    def exposed_get_players(self):
        return self._players

    def _init_world(self):
        x, y = self._dim
        self._world = [[choices([0, 2], [1 - self._sweet_probability, self._sweet_probability])[0] for _ in range(x)]
                       for _ in range(y)]


if __name__ == '__main__':
    """
        note: we can chose ThreadedServer, ForkingServer or even ThreadedPoolServer
        depending on the OS. Forking only works with UNIX based OS
    """

    world_dim = (10, 10)
    game_server = GameServer(world_dim)
    server = ThreadedServer(game_server, port=12345)
    print(game_server)
    server.start()
