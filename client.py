import rpyc
import os
import tkinter as tk


class Display():

    def __init__(self, rows, columns, sizeOfCase):
        self._rows = rows
        self._columns = columns
        self._sizeOfCase = sizeOfCase
        self._damier = tk.Canvas(width=self._rows * self._sizeOfCase, height=self._columns * self._sizeOfCase)
        for k in range(0, self._rows):
            self._damier.create_line(self._sizeOfCase * k, 0, self._sizeOfCase * k, self._rows * self._sizeOfCase,
                                     width=1)
            self._damier.create_line(0, self._sizeOfCase * k, self._columns * self._sizeOfCase, self._sizeOfCase * k,
                                     width=1)
        self._damier.pack()

    def draw(self, grid):
        self._grid = grid
        for x in range(0, len(self._grid)):
            for y in range(0, len(self._grid[x])):
                if (self._grid[x][y] == 1):
                    self._damier.create_rectangle(x * self._sizeOfCase, y * self._sizeOfCase,
                                                  (x + 1) * self._sizeOfCase, (y + 1) * self._sizeOfCase, fill='red')
                if (self._grid[x][y] == 2):
                    self._damier.create_rectangle(x * self._sizeOfCase, y * self._sizeOfCase,
                                                  (x + 1) * self._sizeOfCase, (y + 1) * self._sizeOfCase, fill='green')

    def rightKey(event):
        print("Right key pressed")

    def leftKey(event):
        print("Left key pressed")

    def topKey(event):
        print("Top key pressed")

    def botKey(event):
        print("Bot key pressed")


def bind():
    damier.bind_all('<Right>', rightKey)
    damier.bind_all('<Left>', leftKey)
    damier.bind_all('<Up>', topKey)
    damier.bind_all('<Down>', botKey)
    damier.pack()


class GameClient(rpyc.Service):

    def exposed_notify_new_player(self, number):
        print('new player', number)


if __name__ == '__main__':
    conn = rpyc.connect('127.0.0.1', 12345, service=GameClient)
    conn2 = rpyc.connect('127.0.0.1', 12345, service=GameClient)
    # print(conn.root.exposed_get_players())
    # os.system('pause')
    rows = columns = 10
    sizeOfCase = 30
    tab1 = [0, 1, 0, 0, 1, 2, 0, 2, 0, 0]
    tab2 = [0, 0, 0, 2, 0, 1, 2, 0, 0, 1]
    tab = [tab1, tab2, tab1, tab2, tab1, tab2, tab1, tab2, tab1, tab2]
    disp = Display(rows, columns, sizeOfCase)
    disp.draw(tab)
    tk.mainloop()
