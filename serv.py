import rpyc
from rpyc.utils.server import ThreadedServer # or ForkingServer


class MyService(rpyc.Service):
    
    _players = []
    _grid = []

    def on_connect(self):
        self._players.append(self._conn)
        print('new player:', self._conn)

    def on_disconnect(self):
        self._players.remove(self._conn)
        print('player left:', self._conn)


if __name__ == "__main__":

    """
        note: we can chose ThreadedServer, ForkingServer or even ThreadedPoolServer
    """

    server = ThreadedServer(MyService, port=12345)
    server.start()
