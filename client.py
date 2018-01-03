import rpyc
import os
import tkinter as tk
import time


class GameClient(rpyc.Service):

    def on_connect(self):
        self._rows = 10
        self._columns = 10
        self._sizeOfCase = 30
        self._damier = tk.Canvas(width=self._rows * self._sizeOfCase, height=self._columns * self._sizeOfCase)
        for k in range(0, self._rows):
            self._damier.create_line(self._sizeOfCase * k, 0, self._sizeOfCase * k, self._rows * self._sizeOfCase,
                                     width=1)
            self._damier.create_line(0, self._sizeOfCase * k, self._columns * self._sizeOfCase, self._sizeOfCase * k,
                                     width=1)
        self.bind()
        self._damier.pack()
        self._conn.root.start_game()

    def draw(self, grid):
        t1 = time.time()
        self._grid = grid
        for x in range(0, len(self._grid)):
            for y in range(0, len(self._grid[x])):
                if (self._grid[x][y] == 0):
                    self._damier.create_rectangle(x * self._sizeOfCase, y * self._sizeOfCase,
                                                  (x + 1) * self._sizeOfCase, (y + 1) * self._sizeOfCase, fill='white')
                if (self._grid[x][y] == 1):
                    self._damier.create_rectangle(x * self._sizeOfCase, y * self._sizeOfCase,
                                                  (x + 1) * self._sizeOfCase, (y + 1) * self._sizeOfCase, fill='red')
                if (self._grid[x][y] == 2):
                    self._damier.create_rectangle(x * self._sizeOfCase, y * self._sizeOfCase,
                                                  (x + 1) * self._sizeOfCase, (y + 1) * self._sizeOfCase, fill='green')
        print(time.time() - t1)

    def rightKey(self, event):
        print("Right key pressed")
        self._conn.root.start_game()

    def leftKey(self, event):
        print("Left key pressed")

    def topKey(self, event):
        print("Top key pressed")

    def botKey(self, event):
        print("Bot key pressed")

    def bind(self):
        self._damier.bind_all('<Right>', self.rightKey)
        self._damier.bind_all('<Left>', self.leftKey)
        self._damier.bind_all('<Up>', self.topKey)
        self._damier.bind_all('<Down>', self.botKey)
        self._damier.pack()

    def exposed_draw(self, grid):
        print("test")
        self.draw(grid)

    def exposed_notify_new_player(self, player_name):
        print('new player joined the game', player_name)

    def exposed_notify_player_left(self, player_name):
        print('a player left the game', player_name)

if __name__ == '__main__':
    conn = rpyc.connect('127.0.0.1', 12345, service=GameClient)
    # conn.root.exposed_start_game()
    # conn2 = rpyc.connect('127.0.0.1', 12345, service=GameClient)
    # print(conn.root.exposed_get_players())
    tk.mainloop()

    # os.system('pause')
    # rows = columns = 10
    # sizeOfCase = 30
    # tab1 = [0, 1, 0, 0, 1, 2, 0, 2, 0, 0]
    # tab2 = [0, 0, 0, 2, 0, 1, 2, 0, 0, 1]
    # tab = [tab1, tab2, tab1, tab2, tab1, tab2, tab1, tab2, tab1, tab2]
    # disp = Display(rows, columns, sizeOfCase)
    # disp.draw(tab)
