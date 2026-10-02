# Road network data for the Emergency Route Planner

locations = {
    "Hospital": {
        "lat": 17.4065,
        "lon": 78.4772
    },
    "Location A": {
        "lat": 17.4120,
        "lon": 78.4800
    },
    "Location B": {
        "lat": 17.4150,
        "lon": 78.4850
    },
    "Location C": {
        "lat": 17.4100,
        "lon": 78.4900
    },
    "Location D": {
        "lat": 17.4020,
        "lon": 78.4880
    },
    "Location E": {
        "lat": 17.3980,
        "lon": 78.4820
    },
    "Location F": {
        "lat": 17.4000,
        "lon": 78.4750
    }
}


# Graph
# Each road contains:
# distance = kilometers
# time = normal travel time in minutes
# traffic = traffic multiplier

roads = {
    "Hospital": [
        {"node": "Location A", "distance": 1.5, "time": 4, "traffic": 1.0},
        {"node": "Location D", "distance": 2.2, "time": 5, "traffic": 1.2}
    ],

    "Location A": [
        {"node": "Hospital", "distance": 1.5, "time": 4, "traffic": 1.0},
        {"node": "Location B", "distance": 1.8, "time": 5, "traffic": 1.5},
        {"node": "Location F", "distance": 2.0, "time": 5, "traffic": 1.0}
    ],

    "Location B": [
        {"node": "Location A", "distance": 1.8, "time": 5, "traffic": 1.5},
        {"node": "Location C", "distance": 1.6, "time": 4, "traffic": 1.0},
        {"node": "Location D", "distance": 2.5, "time": 6, "traffic": 1.3}
    ],

    "Location C": [
        {"node": "Location B", "distance": 1.6, "time": 4, "traffic": 1.0},
        {"node": "Location D", "distance": 1.4, "time": 4, "traffic": 1.8}
    ],

    "Location D": [
        {"node": "Hospital", "distance": 2.2, "time": 5, "traffic": 1.2},
        {"node": "Location B", "distance": 2.5, "time": 6, "traffic": 1.3},
        {"node": "Location C", "distance": 1.4, "time": 4, "traffic": 1.8},
        {"node": "Location E", "distance": 1.7, "time": 4, "traffic": 1.0}
    ],

    "Location E": [
        {"node": "Location D", "distance": 1.7, "time": 4, "traffic": 1.0},
        {"node": "Location F", "distance": 1.5, "time": 4, "traffic": 1.2}
    ],

    "Location F": [
        {"node": "Location E", "distance": 1.5, "time": 4, "traffic": 1.2},
        {"node": "Location A", "distance": 2.0, "time": 5, "traffic": 1.0}
    ]
}