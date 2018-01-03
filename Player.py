class Player:
    __init__(self, x, y, name):
        self._x = x
        self._y = y
        self._name = name
        self._score = 0
        
    getPos(self):
        return (self._x, self._y)
        
    setPos(self, x, y):
        self._x = x
        self._y = y
        
    getScore(self):
        return self._score
        
    setScore(self, score):
        self._score = score
        
    __repr__(self):
        print("Player : " + self._name + ", Coordonnées : (" + self._x + "," + self._y + "), Score : " + self._score)
