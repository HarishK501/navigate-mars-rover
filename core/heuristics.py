import math


class Heuristic:
    def __init__(self, heuristic):
        self.heuristic = heuristic

    def calculate(self, dx, dy):
        if self.heuristic == "manhattan":
            return dx + dy
        elif self.heuristic == "euclidean":
            return math.sqrt(dx * dx + dy * dy)
        elif self.heuristic == "octile":
            x = math.sqrt(2) - 1
            if dx < dy:
                return x * dx + dy
            else:
                return x * dy + dx
        elif self.heuristic == "chebyshev":
            return max(dx, dy)
