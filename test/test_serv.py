from mock import MagicMock
from src.serv import GameServer
from src.client import GameClient
from rpyc.utils.server import ThreadedServer
import threading
import rpyc

if __name__ == '__main__':

    """
        In this module we mock client calls to assert server servcice behaviours
    """

    mock_client = GameClient(None)
    mock_client.exposed_notify_new_player = MagicMock(return_value='valeur bid0n')

    t = ThreadedServer(GameServer, port=8686)

    print('here before')
    serv_thread = threading.Thread(target=t.start)
    serv_thread.start()
    print('here')
    conn = rpyc.connect('127.0.0.1', 8686, service=GameClient)
    print(conn.root.exposed_start_game('toto'))
