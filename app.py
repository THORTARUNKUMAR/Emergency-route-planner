from flask import Flask, request, jsonify
from flask_cors import CORS

from graphdata import locations, roads

from algorithms import (
    bfs,
    dfs,
    greedy_best_first,
    a_star
)


app = Flask(__name__)

CORS(app)


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------

@app.route("/")
def home():

    return jsonify({
        "message": "Intelligent Emergency Route Planner API is running!"
    })


# ---------------------------------------------------------
# GET LOCATIONS
# ---------------------------------------------------------

@app.route("/api/locations")
def get_locations():

    return jsonify(locations)


# ---------------------------------------------------------
# FIND ROUTE
# ---------------------------------------------------------

@app.route("/api/route", methods=["POST"])
def find_route():

    data = request.get_json()

    start = data.get("start")
    goal = data.get("goal")
    algorithm = data.get("algorithm", "astar")

    if not start or not goal:

        return jsonify({
            "error": "Start and destination are required."
        }), 400

    if start not in roads or goal not in roads:

        return jsonify({
            "error": "Invalid location."
        }), 400

    if algorithm == "bfs":

        result = bfs(
            roads,
            start,
            goal
        )

    elif algorithm == "dfs":

        result = dfs(
            roads,
            start,
            goal
        )

    elif algorithm == "greedy":

        result = greedy_best_first(
            roads,
            locations,
            start,
            goal
        )

    elif algorithm == "astar":

        result = a_star(
            roads,
            locations,
            start,
            goal
        )

    else:

        return jsonify({
            "error": "Invalid algorithm."
        }), 400

    if result is None:

        return jsonify({
            "error": "No route found."
        }), 404

    return jsonify(result)


# ---------------------------------------------------------
# COMPARE ALL ALGORITHMS
# ---------------------------------------------------------

@app.route("/api/compare", methods=["POST"])
def compare_algorithms():

    data = request.get_json()

    start = data.get("start")
    goal = data.get("goal")

    if not start or not goal:

        return jsonify({
            "error": "Start and destination are required."
        }), 400

    results = {}

    results["BFS"] = bfs(
        roads,
        start,
        goal
    )

    results["DFS"] = dfs(
        roads,
        start,
        goal
    )

    results["Greedy Best-First"] = greedy_best_first(
        roads,
        locations,
        start,
        goal
    )

    results["A*"] = a_star(
        roads,
        locations,
        start,
        goal
    )

    return jsonify(results)


# ---------------------------------------------------------
# RUN SERVER
# ---------------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )