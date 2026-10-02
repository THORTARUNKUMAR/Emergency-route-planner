from collections import deque
import heapq
import math


def get_edge(graph, current, neighbor):
    for edge in graph[current]:
        if edge["node"] == neighbor:
            return edge
    return None


def calculate_path_details(graph, path):
    total_distance = 0
    total_time = 0

    for i in range(len(path) - 1):
        edge = get_edge(graph, path[i], path[i + 1])

        if edge:
            total_distance += edge["distance"]

            # Traffic affects travel time
            total_time += edge["time"] * edge["traffic"]

    return round(total_distance, 2), round(total_time, 2)


# ---------------------------------------------------------
# BFS
# ---------------------------------------------------------

def bfs(graph, start, goal):

    queue = deque([[start]])
    visited = {start}

    nodes_explored = 0

    while queue:

        path = queue.popleft()
        current = path[-1]

        nodes_explored += 1

        if current == goal:
            distance, time = calculate_path_details(graph, path)

            return {
                "path": path,
                "distance": distance,
                "time": time,
                "nodes_explored": nodes_explored
            }

        for edge in graph[current]:

            neighbor = edge["node"]

            if neighbor not in visited:

                visited.add(neighbor)

                new_path = path + [neighbor]

                queue.append(new_path)

    return None


# ---------------------------------------------------------
# DFS
# ---------------------------------------------------------

def dfs(graph, start, goal):

    stack = [[start]]
    visited = set()

    nodes_explored = 0

    while stack:

        path = stack.pop()

        current = path[-1]

        if current in visited:
            continue

        visited.add(current)

        nodes_explored += 1

        if current == goal:

            distance, time = calculate_path_details(graph, path)

            return {
                "path": path,
                "distance": distance,
                "time": time,
                "nodes_explored": nodes_explored
            }

        # Reverse so the order looks natural
        for edge in reversed(graph[current]):

            neighbor = edge["node"]

            if neighbor not in visited:

                stack.append(path + [neighbor])

    return None


# ---------------------------------------------------------
# Heuristic
# Straight-line distance between two locations
# ---------------------------------------------------------

def heuristic(locations, current, goal):

    lat1 = math.radians(locations[current]["lat"])
    lon1 = math.radians(locations[current]["lon"])

    lat2 = math.radians(locations[goal]["lat"])
    lon2 = math.radians(locations[goal]["lon"])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    earth_radius = 6371

    return earth_radius * c


# ---------------------------------------------------------
# Greedy Best-First Search
# ---------------------------------------------------------

def greedy_best_first(graph, locations, start, goal):

    priority_queue = []

    counter = 0

    heapq.heappush(
        priority_queue,
        (heuristic(locations, start, goal), counter, start, [start])
    )

    visited = set()

    nodes_explored = 0

    while priority_queue:

        _, _, current, path = heapq.heappop(priority_queue)

        if current in visited:
            continue

        visited.add(current)

        nodes_explored += 1

        if current == goal:

            distance, time = calculate_path_details(graph, path)

            return {
                "path": path,
                "distance": distance,
                "time": time,
                "nodes_explored": nodes_explored
            }

        for edge in graph[current]:

            neighbor = edge["node"]

            if neighbor not in visited:

                counter += 1

                h = heuristic(locations, neighbor, goal)

                heapq.heappush(
                    priority_queue,
                    (h, counter, neighbor, path + [neighbor])
                )

    return None


# ---------------------------------------------------------
# A* SEARCH
#
# f(n) = g(n) + h(n)
# ---------------------------------------------------------

def a_star(graph, locations, start, goal):

    priority_queue = []

    counter = 0

    g_score = {
        start: 0
    }

    heapq.heappush(
        priority_queue,
        (heuristic(locations, start, goal), counter, start, [start])
    )

    visited = set()

    nodes_explored = 0

    while priority_queue:

        f_score, _, current, path = heapq.heappop(priority_queue)

        if current in visited:
            continue

        visited.add(current)

        nodes_explored += 1

        if current == goal:

            distance, time = calculate_path_details(graph, path)

            return {
                "path": path,
                "distance": distance,
                "time": time,
                "nodes_explored": nodes_explored
            }

        for edge in graph[current]:

            neighbor = edge["node"]

            # Cost considers traffic
            road_cost = edge["time"] * edge["traffic"]

            tentative_g = g_score[current] + road_cost

            if neighbor not in g_score or tentative_g < g_score[neighbor]:

                g_score[neighbor] = tentative_g

                counter += 1

                h = heuristic(locations, neighbor, goal)

                f = tentative_g + h

                heapq.heappush(
                    priority_queue,
                    (
                        f,
                        counter,
                        neighbor,
                        path + [neighbor]
                    )
                )

    return None