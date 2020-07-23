import math
from heuristics import Heuristic
from gridGraph import myGrid
from pathBinder import pathBinder


class AStarFinder:
    def __init__(self, start, end, blocks, options, heuristic, weight):
        myGrid.refresh()
        self.start = myGrid.getNode(int(start['x']), int(start['y']))
        self.end = myGrid.getNode(int(end['x']), int(end['y']))
        myGrid.setBlocks(blocks)
        self.allowDiagonal = False
        self.bidirectional = False
        self.setOptions(options)
        if heuristic != -1:
            self.heuristic = Heuristic(heuristic)
        else:
            self.heuristic = None
        self.weight = int(weight)

    def find(self):
        if self.bidirectional:
            return self.find2()
        return self.find1()

    def setOptions(self, options):
        if len(options) == 2:
            self.allowDiagonal = True
            self.bidirectional = True
        elif len(options) == 1:
            if options[0] == 'allow-diagonal':
                self.allowDiagonal = True
            elif options[0] == 'bi-directional':
                self.bidirectional = True

    def find1(self):
        G = {}  # Actual movement cost to each position from the start position
        H = {}  # heuristic cost
        F = {}  # Estimated movement cost of start to end going via this position

        # source point
        x1, y1 = self.start.getPosition()

        # destination point
        x2, y2 = self.end.getPosition()

        discover = []

        G[self.start] = 0
        if self.heuristic is not None:
            H[self.start] = self.heuristic.calculate(abs(x1 - x2), abs(y1 - y2))
        else:
            H[self.start] = 0
        F[self.start] = H[self.start]

        closedVertices = set()
        openVertices = set()
        openVertices.add(self.start)
        cameFrom = {}

        while len(openVertices) > 0:
            # Get the vertex in the open list with the lowest F score
            curNode = None
            currentFScore = None

            for item in openVertices:
                if curNode is None or F[item] < currentFScore:
                    curNode = item
                    currentFScore = F[item]

            # Check if we have reached the goal
            x, y = curNode.getPosition()

            if x == x2 and y == y2:
                return discover, curNode.backtrace(cameFrom)

            openVertices.remove(curNode)
            closedVertices.add(curNode)

            if self.allowDiagonal:
                neighbourNodes = curNode.getNeighbours()
            else:
                neighbourNodes = curNode.getNonDiagonalNeighbours()

            # Update scores for vertices near the current position
            for i in neighbourNodes:
                if i.isWalkableFrom(curNode):
                    a, b = i.getPosition()
                    if i in closedVertices:
                        continue

                    if a-x == 0 or b-y == 0:    # non-diagonal
                        p = 1
                    else:
                        p = math.sqrt(2)

                    candidateG = G[curNode] + p

                    if i not in openVertices:
                        discover.append(str(i))
                        openVertices.add(i)
                    elif candidateG >= G[i]:
                        continue

                    cameFrom[i] = curNode
                    G[i] = candidateG
                    if i not in H:
                        if self.heuristic is not None:
                            H[i] = self.heuristic.calculate(abs(a - x2), abs(b - y2)) * self.weight   # heuristic function
                        else:
                            H[i] = 0
                    F[i] = G[i] + H[i]

        return discover, []

    def find2(self):
        G1 = {}  # Actual movement cost to each position from the start position
        H1 = {}  # heuristic cost
        F1 = {}  # Estimated movement cost of start to end going via this position

        G2 = {}
        H2 = {}
        F2 = {}

        # source point
        x1, y1 = self.start.getPosition()

        # destination point
        x2, y2 = self.end.getPosition()

        discover1 = []
        discover2 = []

        G1[self.start] = 0
        if self.heuristic is not None:
            H1[self.start] = self.heuristic.calculate(abs(x1 - x2), abs(y1 - y2))
        else:
            H1[self.start] = 0
        F1[self.start] = H1[self.start]

        G2[self.end] = 0
        H2[self.end] = H1[self.start]
        F2[self.end] = H1[self.start]

        closedVertices_st = set()
        openVertices_st = set()

        closedVertices_end = set()
        openVertices_end = set()

        openVertices_st.add(self.start)
        cameFrom_st = {}

        openVertices_end.add(self.end)
        cameFrom_end = {}

        # path = pathBinder(curNodeStart.backtrace(cameFromStart), i.backtrace(cameFromEnd, reverse=False))

        while len(openVertices_st) > 0 and len(openVertices_end) > 0:
            # start part
            curNode = None
            currentFScore_st = None

            for item in openVertices_st:
                if curNode is None or F1[item] < currentFScore_st:
                    curNode = item
                    currentFScore_st = F1[item]

            x, y = curNode.getPosition()

            openVertices_st.remove(curNode)
            closedVertices_st.add(curNode)

            if self.allowDiagonal:
                neighbourNodes = curNode.getNeighbours()
            else:
                neighbourNodes = curNode.getNonDiagonalNeighbours()

            # Update scores for vertices near the current position
            for i in neighbourNodes:
                if i.isWalkableFrom(curNode):
                    a, b = i.getPosition()
                    if i in closedVertices_st:
                        continue

                    if a - x == 0 or b - y == 0:  # non-diagonal
                        p = 1
                    else:
                        p = math.sqrt(2)

                    candidateG = G1[curNode] + p

                    if i not in openVertices_st:
                        discover1.append(str(i))
                        openVertices_st.add(i)
                        if i in closedVertices_end:
                            path = pathBinder(curNode.backtrace(cameFrom_st),
                                              i.backtrace(cameFrom_end, reverse=False))
                            discover = ["bidirectional", discover1, discover2]
                            return discover, path
                    elif candidateG >= G1[i]:
                        continue

                    cameFrom_st[i] = curNode
                    G1[i] = candidateG
                    if i not in H1:
                        if self.heuristic is not None:
                            H1[i] = self.heuristic.calculate(abs(a - x2), abs(b - y2)) * self.weight  # heuristic function
                        else:
                            H1[i] = 0
                    F1[i] = G1[i] + H1[i]

            # end part------------------------------------------------------------------------------------------------

            curNode = None
            currentFScore_end = None

            for item in openVertices_end:
                if curNode is None or F2[item] < currentFScore_end:
                    curNode = item
                    currentFScore_end = F2[item]

            x, y = curNode.getPosition()

            openVertices_end.remove(curNode)
            closedVertices_end.add(curNode)

            if self.allowDiagonal:
                neighbourNodes = curNode.getNeighbours()
            else:
                neighbourNodes = curNode.getNonDiagonalNeighbours()

            # Update scores for vertices near the current position
            for i in neighbourNodes:
                if i.isWalkableFrom(curNode):
                    a, b = i.getPosition()
                    if i in closedVertices_end:
                        continue

                    if a - x == 0 or b - y == 0:  # non-diagonal
                        p = 1
                    else:
                        p = math.sqrt(2)

                    candidateG = G2[curNode] + p

                    if i not in openVertices_end:
                        discover2.append(str(i))
                        openVertices_end.add(i)
                        if i in closedVertices_st:
                            path = pathBinder(i.backtrace(cameFrom_st),
                                              curNode.backtrace(cameFrom_end, reverse=False))
                            discover = ["bidirectional", discover1, discover2]
                            return discover, path
                    elif candidateG >= G2[i]:
                        continue

                    cameFrom_end[i] = curNode
                    G2[i] = candidateG
                    if i not in H2:
                        if self.heuristic is not None:
                            H2[i] = self.heuristic.calculate(abs(a - x1), abs(b - y1)) * self.weight  # heuristic function
                        else:
                            H2[i] = 0

                    F2[i] = G2[i] + H2[i]

        discover = ["bidirectional", discover1, discover2]
        return discover, []
