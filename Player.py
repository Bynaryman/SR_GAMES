class Player:
    def __init__(self, x, y, name, conn):
        self._x = x
        self._y = y
        self._name = name
        self._score = 0
        self._conn = conn

    def getPos(self):
        return self._x, self._y

    def setPos(self, x, y):
        self._x = x
        self._y = y

    def getScore(self):
        return self._score

    def setScore(self, score):
        self._score = score

    def getName(self):
        return self._name

    def getConn(self):
        return self._conn

    def __repr__(self):
        print("Player : " + self._name + ", Coordonnées : (" + self._x + "," + self._y + "), Score : " + self._score)
