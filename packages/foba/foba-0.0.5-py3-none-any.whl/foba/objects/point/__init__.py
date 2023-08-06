from math import sqrt


class Point:
    id = 0

    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        if id is not None: self.id = id

    @property
    def distance(self): return sqrt(self.x ** 2 + self.y ** 2)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        return self

    @staticmethod
    def build(x, y): return Point(x, y)