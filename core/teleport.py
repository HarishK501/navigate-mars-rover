from gridGraph import myGrid
from collections import deque
from pathBinder import pathBinder


class PortFinder:
    def __init__(self, start, end, blocks, options, ports):
        myGrid.refresh()
        self.start = myGrid.getNode(int(start['x']), int(start['y']))
        self.end = myGrid.getNode(int(end['x']), int(end['y']))
        myGrid.setBlocks(blocks)
        self.allowDiagonal = False
        self.setOptions(options)
        self.port1 = myGrid.getNode(int(ports[0]['x']), int(ports[0]['y']))
        self.port2 = myGrid.getNode(int(ports[1]['x']), int(ports[1]['y']))

    def setOptions(self, options):
        if len(options) == 1:
            if options[0] == 'allow-diagonal':
                self.allowDiagonal = True

    def find(self):
        p1_x, p1_y = self.port1.getPosition()
        p2_x, p2_y = self.port2.getPosition()

        # source point
        x1, y1 = self.start.getPosition()

        # destination point
        x2, y2 = self.end.getPosition()

        myGrid.visited[x1][y1] = True

        myGrid.visited2[x2][y2] = True

        cameFromStart = {}
        cameFromEnd = {}

        startQueue = deque()
        discover1 = []
        startQueue.append(self.start)
        endQueue = deque()
        discover2 = []
        endQueue.append(self.end)

        pathFromStart = []
        pathFromEnd = []

        while startQueue or endQueue:
            if startQueue:
                curNodeStart = startQueue.popleft()

                x, y = curNodeStart.getPosition()
                if (x == p1_x and y == p1_y) or (x == p2_x and y == p2_y):
                    pathFromStart = curNodeStart.backtrace(cameFromStart)
                    startQueue = None
                    continue

                if self.allowDiagonal:
                    neighbourNodes = curNodeStart.getNeighbours()
                else:
                    neighbourNodes = curNodeStart.getNonDiagonalNeighbours()

                for i in neighbourNodes:
                    a, b = i.getPosition()

                    if i.isWalkableFrom(curNodeStart) and not myGrid.visited[a][b]:
                        if myGrid.visited2[a][b]:
                            path = pathBinder(curNodeStart.backtrace(cameFromStart), i.backtrace(cameFromEnd, reverse=False))
                            discover = ["bidirectional", discover1, discover2]
                            return discover, path
                        discover1.append(str(i))
                        myGrid.visited[a][b] = True
                        cameFromStart[i] = curNodeStart
                        startQueue.append(i)

            if endQueue:
                curNodeEnd = endQueue.popleft()
                x, y = curNodeEnd.getPosition()
                if (x == p1_x and y == p1_y) or (x == p2_x and y == p2_y):
                    pathFromEnd = curNodeEnd.backtrace(cameFromEnd, reverse=False)
                    endQueue = None
                    continue

                if self.allowDiagonal:
                    neighbourNodes = curNodeEnd.getNeighbours()
                else:
                    neighbourNodes = curNodeEnd.getNonDiagonalNeighbours()

                # neighbourNodes.reverse()

                for i in neighbourNodes:
                    a, b = i.getPosition()
                    if i.isWalkableFrom(curNodeEnd) and not myGrid.visited2[a][b]:
                        if myGrid.visited[a][b]:
                            path = pathBinder(i.backtrace(cameFromStart), curNodeEnd.backtrace(cameFromEnd, reverse=False))
                            discover = ["bidirectional", discover1, discover2]
                            return discover, path
                        discover2.append(str(i))
                        myGrid.visited2[a][b] = True
                        cameFromEnd[i] = curNodeEnd
                        endQueue.append(i)

        if len(pathFromStart) > 0 and len(pathFromEnd) > 0:
            discover = ["bidirectional", discover1, discover2]
            path = ["two-paths", pathFromStart, pathFromEnd]
            return discover, path

        discover = ["bidirectional", discover1, discover2]
        return discover, []   # no path

