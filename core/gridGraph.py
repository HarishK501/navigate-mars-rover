from node import Node


class Graph:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.visited = [[False for i in range(height)] for j in range(width)]
        self.visited2 = [[False for i in range(height)] for j in range(width)]   # for bi-directional search purposes
        self.nodeList = {}
        self.blocks = []

    def getNode(self, x, y):
        if str(x)+" "+str(y) in self.nodeList:
            return self.nodeList[str(x)+" "+str(y)]
        else:
            return -1

    def connectNeighbours(self):
        for node in self.nodeList.values():
            x, y = node.getPosition()
            node.addNeighbour(self.getNode(x + 30, y), 'east')
            node.addNeighbour(self.getNode(x, y - 30), 'north')
            node.addNeighbour(self.getNode(x - 30, y), 'west')
            node.addNeighbour(self.getNode(x, y + 30), 'south')
            node.addNeighbour(self.getNode(x + 30, y - 30), 'ne', diagonal=True)

            node.addNeighbour(self.getNode(x - 30, y - 30), 'nw', diagonal=True)

            node.addNeighbour(self.getNode(x - 30, y + 30), 'sw', diagonal=True)

            node.addNeighbour(self.getNode(x + 30, y + 30), 'se', diagonal=True)

    def generateGrid(self):
        for i in range(0, self.width, 30):
            for j in range(0, self.height, 30):
                self.nodeList[str(i)+' '+str(j)] = Node(i, j)
        self.connectNeighbours()
        return self

    def refresh(self):
        for i in self.blocks:
            i.freeNode()
            # i.parent = None

        self.blocks = []
        self.visited = [[False for x in range(self.height)] for y in range(self.width)]
        self.visited2 = [[False for x in range(self.height)] for y in range(self.width)]

    def setBlocks(self, blocks_dict):
        x = 0
        y = 0
        for i in range(0, len(blocks_dict), 2):
            a = blocks_dict['x'+str(x)]
            b = blocks_dict['y'+str(y)]
            self.blocks.append(self.getNode(a, b))
            self.getNode(a, b).blockNode()
            x += 1
            y += 1

        return


myGrid = Graph(1920, 1080)
myGrid.generateGrid()
