import rpyc
from rpyc.utils.server import ThreadedServer # or ForkingServer


class MyService(rpyc.Service):
    
    _players = []
    _world = []

    def __init__(self,  *args):
        super().__init__(*args)
        self._init_world(self._world)

    def on_connect(self):
        self._players.append(self._conn)
        print('new player:', self._conn)

    def on_disconnect(self):
        self._players.remove(self._conn)
        print('player left:', self._conn)

    def exposed_get_players(self):
        return self._players

    def _init_world(self, world):
        pass


if __name__ == '__main__':

    """
        note: we can chose ThreadedServer, ForkingServer or even ThreadedPoolServer
        depending on the OS. Forking only works with UNIX based OS
    """

    server = ThreadedServer(MyService, port=12345)
    server.start()
