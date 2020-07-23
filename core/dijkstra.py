from Astar import AStarFinder


class DijkstraSearch:
    def __init__(self, dict_data):
        self.dict_data = dict_data

    def find(self):
        D = self.dict_data
        dijkstraFinder = AStarFinder(D['start'], D['end'], D['blocks'], D['options'], heuristic=-1, weight=0)
        a, b = dijkstraFinder.find()
        return a, b

