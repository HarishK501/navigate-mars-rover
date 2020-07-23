# function to return key for any value
def get_key(my_dict, val):
    for key, value in my_dict.items():
        if val == value:
            return key

    return "key doesn't exist"


class Node:
    def __init__(self, x, y, walkable=True):
        self._x = x
        self._y = y
        self._walkable = walkable
        self._neighbours = {}
        self._nonDiagonalNeighbours = {}

    def __str__(self):
        return str(self._x)+" "+str(self._y)

    def getState(self):
        return self._walkable

    def isWalkableFrom(self, curNode):
        if self._walkable:
            rel_position = get_key(curNode.getNeighboursDict(), self)

            dl = ['ne', 'nw', 'se', 'sw']
            if rel_position in dl:
                return self.checkSides(rel_position)
            return True
        return False

    def checkSides(self, rp):
        a = self._neighbours.get('north')
        b = self._neighbours.get('east')
        c = self._neighbours.get('west')
        d = self._neighbours.get('south')
        if a and b and c and d:
            if rp == 'ne':
                if not c.getState() and not d.getState():
                    return False
            elif rp == 'nw':
                if not b.getState() and not d.getState():
                    return False
            elif rp == 'se':
                if not a.getState() and not c.getState():
                    return False
            else:
                if not a.getState() and not b.getState():
                    return False

        return True

    def getPosition(self):
        return self._x, self._y

    def blockNode(self):
        self._walkable = False

    def freeNode(self):
        self._walkable = True

    def addNeighbour(self, n, position, diagonal=False):
        if n != -1:
            if not diagonal:
                self._nonDiagonalNeighbours[position] = n
            self._neighbours[position] = n

    # def resetNeighbours(self):
    #     self._neighbours = []
    #     self._nonDiagonalNeighbours = []

    def getNeighboursDict(self):
        return self._neighbours

    def getNeighbours(self):
        return self._neighbours.values()

    def getNonDiagonalNeighbours(self):
        return self._nonDiagonalNeighbours.values()

    def backtrace(self, cameFrom, reverse=True):
        """
        Backtrace according to the parent records and return the path.
        (including both start and end nodes)
        """
        path = [str(self)]
        node = self
        while node in cameFrom:
            node = cameFrom[node]
            # print(node)
            path.append(str(node))
        if reverse:
            path.reverse()
        # for i in path:
        #     print(i)

        return path
