import unittest

from unittest.mock import MagicMock
from src.serv import GameServer
from src.client import GameClient
from rpyc.utils.server import ThreadedServer
import threading
import rpyc


class TestGameServer(unittest.TestCase):

    def test_notify_new_player(self):

        mock_server = GameServer(None)
        # mock_server.
        t = ThreadedServer(mock_server.__class__, port=8686)
        serv_thread = threading.Thread(target=t.start)
        serv_thread.start()

        conn = rpyc.connect('127.0.0.1', 8686, service=GameClient)
        conn2 = rpyc.connect('127.0.0.1', 8686, service=GameClient)

        # conn.root.exposed_notify_new_player = MagicMock()

        mock_client = GameClient(conn)
        mock_client.exposed_notify_new_player = MagicMock()

        conn.root.start_game('t')
        conn.root.start()
        print('here')

        mock_client.exposed_notify_new_player.assert_called()
        print('after')
        self.assertTrue(True)


if __name__ == '__main__':

    """
        In this module we mock client calls to assert server servcice behaviours
    """
    unittest.main()




