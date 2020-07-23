from heuristics import Heuristic
from gridGraph import myGrid
from pathBinder import pathBinder


class BestFirstSearch:
    def __init__(self, start, end, blocks, options, heuristic):
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

    def find(self):
        if self.bidirectional:
            return self.find2(myGrid)
        return self.find1(myGrid)

    def setOptions(self, options):
        if len(options) == 2:
            self.allowDiagonal = True
            self.bidirectional = True
        elif len(options) == 1:
            if options[0] == 'allow-diagonal':
                self.allowDiagonal = True
            elif options[0] == 'bi-directional':
                self.bidirectional = True

    def find1(self, grid):
        H = {}
        F = {}  # Estimated movement cost of start to end going via this position

        # source point
        x1, y1 = self.start.getPosition()

        # destination point
        x2, y2 = self.end.getPosition()

        discover = []

        H[self.start] = self.heuristic.calculate(abs(x1 - x2), abs(y1 - y2)) * 1000000

        F[self.start] = H[self.start]

        q = set()
        q.add(self.start)
        cameFrom = {}

        while len(q) > 0:
            # Get the vertex in the open list with the lowest F score
            curNode = None
            currentFScore = None

            for item in q:
                if curNode is None or F[item] < currentFScore:
                    curNode = item
                    currentFScore = F[item]

            # Check if we have reached the goal
            x, y = curNode.getPosition()

            if x == x2 and y == y2:
                return discover, curNode.backtrace(cameFrom)

            q.remove(curNode)
            grid.visited[x][y] = True

            if self.allowDiagonal:
                neighbourNodes = curNode.getNeighbours()
            else:
                neighbourNodes = curNode.getNonDiagonalNeighbours()

            # Update scores for vertices near the current position
            for i in neighbourNodes:
                if i.isWalkableFrom(curNode):
                    a, b = i.getPosition()
                    if grid.visited[a][b]:
                        continue

                    if i not in q:
                        discover.append(str(i))
                        q.add(i)
                        cameFrom[i] = curNode

                    if i not in H:
                        H[i] = self.heuristic.calculate(abs(a - x2), abs(b - y2)) * 1000000   # heuristic function
                    F[i] = H[i]

        return discover, []

    def find2(self, grid):
        H1 = {}  # heuristic cost
        F1 = {}  # Estimated movement cost of start to end going via this position

        H2 = {}
        F2 = {}

        # source point
        x1, y1 = self.start.getPosition()

        # destination point
        x2, y2 = self.end.getPosition()

        discover1 = []
        discover2 = []

        H1[self.start] = self.heuristic.calculate(abs(x1 - x2), abs(y1 - y2))
        F1[self.start] = H1[self.start]

        H2[self.end] = H1[self.start]
        F2[self.end] = H2[self.end]

        startSet = set()

        endSet = set()

        startSet.add(self.start)
        cameFrom_st = {}

        endSet.add(self.end)
        cameFrom_end = {}

        while len(startSet) > 0 and len(endSet) > 0:
            # start part -------------------------------------------------------------------------
            curNode = None
            currentFScore_st = None

            for item in startSet:
                if curNode is None or F1[item] < currentFScore_st:
                    curNode = item
                    currentFScore_st = F1[item]

            x, y = curNode.getPosition()

            startSet.remove(curNode)
            grid.visited[x][y] = True

            if self.allowDiagonal:
                neighbourNodes = curNode.getNeighbours()
            else:
                neighbourNodes = curNode.getNonDiagonalNeighbours()

            # Update scores for vertices near the current position
            for i in neighbourNodes:
                a, b = i.getPosition()
                if i.isWalkableFrom(curNode) and not grid.visited[a][b]:
                    grid.visited[a][b] = True
                    if i not in startSet:
                        discover1.append(str(i))
                        startSet.add(i)
                        if grid.visited2[a][b]:
                            path = pathBinder(curNode.backtrace(cameFrom_st),
                                              i.backtrace(cameFrom_end, reverse=False))
                            discover = ["bidirectional", discover1, discover2]
                            return discover, path

                    cameFrom_st[i] = curNode
                    if i not in H1:
                        H1[i] = self.heuristic.calculate(abs(a - x2), abs(b - y2)) * 1000000  # heuristic function
                    F1[i] = H1[i]

            # end part------------------------------------------------------------------------------------------------

            curNode = None
            currentFScore_end = None

            for item in endSet:
                if curNode is None or F2[item] < currentFScore_end:
                    curNode = item
                    currentFScore_end = F2[item]

            x, y = curNode.getPosition()

            endSet.remove(curNode)
            grid.visited2[x][y] = True

            if self.allowDiagonal:
                neighbourNodes = curNode.getNeighbours()
            else:
                neighbourNodes = curNode.getNonDiagonalNeighbours()

            # Update scores for vertices near the current position
            for i in neighbourNodes:
                a, b = i.getPosition()
                if i.isWalkableFrom(curNode) and not grid.visited2[a][b]:
                    grid.visited2[a][b] = True
                    if i not in endSet:
                        discover2.append(str(i))
                        endSet.add(i)
                        if grid.visited[a][b]:
                            path = pathBinder(i.backtrace(cameFrom_st),
                                              curNode.backtrace(cameFrom_end, reverse=False))
                            discover = ["bidirectional", discover1, discover2]
                            return discover, path
                    cameFrom_end[i] = curNode
                    if i not in H2:
                        H2[i] = self.heuristic.calculate(abs(a - x1), abs(b - y1)) * 1000000  # heuristic function

                    F2[i] = H2[i]

        discover = ["bidirectional", discover1, discover2]
        return discover, []
