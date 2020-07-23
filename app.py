from flask import Flask, render_template, jsonify, request, make_response

from _datetime import datetime as dt

import sys
sys.path.insert(0, 'core')

from core.breadthFirst import BFS
from core.Astar import AStarFinder
from core.best_first import BestFirstSearch
from core.dijkstra import DijkstraSearch
from core.teleport import PortFinder

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/path-finding")
def grid():
    return render_template("path-finding.html")


@app.route("/get_data", methods=['POST'])
def get_data():
    entry_dict = request.get_json()
    travel, path, c = [], [], 0
    if entry_dict['algo'] == "BFS":
        a = dt.now()
        travel, path = BFS(entry_dict['start'], entry_dict['end'], entry_dict['blocks'], entry_dict['options']).find()
        b = dt.now()
        c = b-a

    elif entry_dict['algo'] == "a-star":
        a = dt.now()
        travel, path = AStarFinder(entry_dict['start'], entry_dict['end'], entry_dict['blocks'], entry_dict['options'], entry_dict['heuristic'], entry_dict['weight']).find()
        b = dt.now()
        c = b-a

    elif entry_dict['algo'] == "Dijkstra":
        a = dt.now()
        travel, path = DijkstraSearch(entry_dict).find()
        b = dt.now()
        c = b-a

    elif entry_dict['algo'] == "best-first":
        a = dt.now()
        travel, path = BestFirstSearch(entry_dict['start'], entry_dict['end'], entry_dict['blocks'], entry_dict['options'], entry_dict['heuristic']).find()
        b = dt.now()
        c = b-a

    elif entry_dict['algo'] == "Teleport":
        a = dt.now()
        travel, path = PortFinder(entry_dict['start'], entry_dict['end'], entry_dict['blocks'], entry_dict['options'], entry_dict['ports']).find()
        b = dt.now()
        c = b-a

    result = {
        'traversal': travel,
        'path': path,
        'time': c.microseconds/1000
    }
    res = make_response(jsonify(result), 200)
    return res


if __name__ == "__main__":
    app.run()




