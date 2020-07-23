from gridGraph import myGrid
from collections import deque
from pathBinder import pathBinder


class BFS:
    def __init__(self, start, end, blocks, options):
        myGrid.refresh()
        self.start = myGrid.getNode(int(start['x']), int(start['y']))
        self.end = myGrid.getNode(int(end['x']), int(end['y']))
        myGrid.setBlocks(blocks)
        self.allowDiagonal = False
        self.bidirectional = False
        self.setOptions(options)

    def setOptions(self, options):
        if len(options) == 2:
            self.allowDiagonal = True
            self.bidirectional = True
        elif len(options) == 1:
            if options[0] == 'allow-diagonal':
                self.allowDiagonal = True
            elif options[0] == 'bi-directional':
                self.bidirectional = True

    def find(self):
        if self.bidirectional:
            return self.find2(myGrid)
        return self.find1(myGrid)

    def find1(self, grid):
        # source point
        x1, y1 = self.start.getPosition()

        # destination point
        x2, y2 = self.end.getPosition()

        cameFrom = {}

        grid.visited[x1][y1] = True

        q = deque()
        discover = []

        q.append(self.start)
        while q:
            curNode = q.popleft()
            x, y = curNode.getPosition()

            if x == x2 and y == y2:
                return discover, curNode.backtrace(cameFrom)

            if self.allowDiagonal:
                neighbourNodes = curNode.getNeighbours()
            else:
                neighbourNodes = curNode.getNonDiagonalNeighbours()

            for i in neighbourNodes:
                a, b = i.getPosition()
                if i.isWalkableFrom(curNode) and not grid.visited[a][b]:
                    discover.append(str(i))
                    grid.visited[a][b] = True
                    cameFrom[i] = curNode
                    q.append(i)
        return discover, []

    def find2(self, grid):      # bi-directional BFS
        # source point
        x1, y1 = self.start.getPosition()

        # destination point
        x2, y2 = self.end.getPosition()

        grid.visited[x1][y1] = True

        grid.visited2[x2][y2] = True

        cameFromStart = {}
        cameFromEnd = {}

        startQueue = deque()
        discover1 = []
        startQueue.append(self.start)
        endQueue = deque()
        discover2 = []
        endQueue.append(self.end)

        while startQueue or endQueue:
            if startQueue:
                curNodeStart = startQueue.popleft()

                if self.allowDiagonal:
                    neighbourNodes = curNodeStart.getNeighbours()
                else:
                    neighbourNodes = curNodeStart.getNonDiagonalNeighbours()

                for i in neighbourNodes:
                    a, b = i.getPosition()
                    if i.isWalkableFrom(curNodeStart) and not grid.visited[a][b]:
                        if grid.visited2[a][b]:
                            path = pathBinder(curNodeStart.backtrace(cameFromStart), i.backtrace(cameFromEnd, reverse=False))
                            discover = ["bidirectional", discover1, discover2]
                            return discover, path
                        discover1.append(str(i))
                        grid.visited[a][b] = True
                        cameFromStart[i] = curNodeStart
                        startQueue.append(i)

            if endQueue:
                curNodeEnd = endQueue.popleft()

                if self.allowDiagonal:
                    neighbourNodes = curNodeEnd.getNeighbours()
                else:
                    neighbourNodes = curNodeEnd.getNonDiagonalNeighbours()

                # neighbourNodes.reverse()

                for i in neighbourNodes:
                    a, b = i.getPosition()
                    if i.isWalkableFrom(curNodeEnd) and not grid.visited2[a][b]:
                        if grid.visited[a][b]:
                            path = pathBinder(i.backtrace(cameFromStart), curNodeEnd.backtrace(cameFromEnd, reverse=False))
                            discover = ["bidirectional", discover1, discover2]
                            return discover, path
                        discover2.append(str(i))
                        grid.visited2[a][b] = True
                        cameFromEnd[i] = curNodeEnd
                        endQueue.append(i)

        discover = ["bidirectional", discover1, discover2]
        return discover, []   # no path
