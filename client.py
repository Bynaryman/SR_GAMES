import rpyc
import os


if __name__ == '__main__':

    conn = rpyc.connect('127.0.0.1', 12345)
    conn2 = rpyc.connect('127.0.0.1', 12345)
    print(conn.root.exposed_get_players())
    os.system('pause')
