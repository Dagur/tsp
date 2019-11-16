import re
from collections import deque
from math import sqrt

import networkx as nx
import plotly.graph_objects as go


def dist(p, q):
    """
    Calculate Euclidian distance to use as weight

    Borrowed from https://docs.python.org/3.8/library/math.html#math.dist
    """
    return sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))


def weighted_edges(points):
    """
    Create an iterable of edges and weight from an iterable of points
    """
    size = len(points)
    return [
        (point, destination, dist(points[point], points[destination]))
        for point in range(size)
        for destination in range(point + 1, size)
    ]


def to_graph(weighted_edges):
    """
    Create a graph object using networkx
    """
    G = nx.Graph()
    G.add_weighted_edges_from(weighted_edges)
    return G


def to_distance_matrix(graph):
    """
    Calculate distance matrix.
    """
    return nx.to_numpy_matrix(graph).A


def plot(points, tour):
    """
    Graphicly display the tour
    """
    fig = go.Figure()
    visited = list(points[int(point)] for point in tour)

    fig.add_trace(
        go.Scatter(x=tuple(x for x, y in visited), y=tuple(y for x, y in visited))
    )

    fig.update_layout(
        width=800,
        height=500,
        title="fixed-ratio axes",
        yaxis=dict(scaleanchor="x", scaleratio=1,),
    )

    fig.show()


def load_tsp(filename):
    """
    Open a .tsp file and grab every line with three numbers (index, and two coordinates)
    Returns an iterable of pairs of ints
    """
    rex = re.compile(r"\s*(\d+)\s+(\d+)\s+(\d+).*")
    lines = deque([])

    with open(filename, "rt") as f:
        for line in f.readlines():
            m = rex.match(str(line))
            if m:
                lines.append((int(m.group(2)), int(m.group(3))))

    return lines
