from itertools import product
from math import log

import numpy

from .tools import to_distance_matrix, to_graph, weighted_edges


def flatten(tour):
    """
    brute_force returns a structures that looks like this
    (((min_cost, node), node), node)
    This function turns it into the tuple (cost, [node, node, node])
    (so not "flatten" in the traditional sense)
    """
    flat_tour = []

    def f(tour):
        (val, node) = tour
        flat_tour.append(node)
        if isinstance(val, tuple):
            return f(val)
        return val

    return (f(tour), flat_tour)


def bits(n):
    """
    Get all 1 bits in a number
    https://stackoverflow.com/questions/8898807/pythonic-way-to-iterate-over-bits-of-integer
    """
    while n:
        b = n & (~n + 1)
        yield b
        n ^= b


def index(node):
    """
    Get index in matrix from binary value. This could be memoized
    """
    return int(log(node, 2))


def brute_force(points):
    """
    Try every possible path and return the lowest cost (Hameltonian cycle)
    """
    edges = weighted_edges(points)
    graph = to_graph(edges)
    matrix = to_distance_matrix(graph)
    start_node = 0
    size = matrix[0].size
    nodes = (1 << size) - 1

    def path(node, total, visited):
        # Track where we are, what the total cost is and which nodes we
        # haven't visited yet
        unvisited = nodes ^ visited
        if unvisited == 0:
            # Complete the cycle back to start and return the total cost of
            # this path
            return (total + matrix[node][start_node], node)

        cost = min(
            path(index(nnode), total + matrix[node][index(nnode)], (visited | nnode))
            for nnode in bits(unvisited)
        )
        return (cost, node)

    tour = path(start_node, 0, 0)
    return flatten(tour)


############################
# Dynamic programming method
############################
def dynamic_setup(matrix, size):
    """
    Create a memoized data structure for all subpaths
    """
    memo = numpy.zeros((size, 1 << size))
    for i in range(1, size):
        memo[i][1 | 1 << i] = matrix[0][i]

    return memo


def combinations(set_bits, length):
    """
    Return all combinations of binary numbers of "length" with "set_bits" number of 1's

    example: combinations(3, 4) returns (0111, 1110, 1011, 1101)
    """
    return (
        int("".join(str(x) for x in combo), 2)
        for combo in product([0, 1], repeat=length)
        if combo.count(1) == set_bits
    )


def not_in(node, subset):
    """
    Is node not a member of subset
    """
    return ((1 << node) & subset) == 0


def dynamic_solve(matrix, memo, size):
    """
    Solve the problem using the initialized memo structure and the distance matrix
    """
    start_node = 0

    for depth in range(3, size + 1):
        for subset in combinations(depth, size):
            if not_in(start_node, subset):
                continue
            for next in range(size):
                if next == start_node or not_in(next, subset):
                    continue
                state = subset ^ (1 << next)
                min_dist = None
                for endpoint in range(size):
                    if (
                        endpoint == start_node
                        or endpoint == next
                        or not_in(endpoint, subset)
                    ):
                        continue
                    new_dist = memo[endpoint][state] + matrix[endpoint][next]
                    if min_dist is None or new_dist < min_dist:
                        min_dist = new_dist
                    memo[next][subset] = min_dist

    return memo


def find_min_cost(matrix, memo, size):
    """
    Find the lowest cost hameltonian cycle
    """
    end_state = (1 << size) - 1
    minimum_tour_cost = None

    for endpoint in range(1, size):
        tour_cost = memo[endpoint][end_state] + matrix[endpoint][0]
        if minimum_tour_cost is None or tour_cost < minimum_tour_cost:
            minimum_tour_cost = tour_cost

    return minimum_tour_cost


def find_optimal_tour(matrix, memo, size):
    """
    Get a route or tour with the lowest cost
    """
    last_index = 0
    state = (1 << size) - 1
    tour = numpy.zeros(size + 1)

    for i in range(size - 1, 0, -1):
        index = -1
        for j in range(1, size):
            if not_in(j, state):
                continue
            if index == -1:
                index = j
            prev_dist = memo[index][state] + matrix[index][last_index]
            new_dist = memo[j][state] + matrix[j][last_index]
            if new_dist < prev_dist:
                index = j

        tour[i] = index
        state = state ^ (1 << index)
        last_index = index

    tour[0] = tour[size] = 0
    return tour


def dynamic(points):
    """
    Speed up the process with dynamic programming.
    """
    edges = weighted_edges(points)
    graph = to_graph(edges)
    matrix = to_distance_matrix(graph)
    size = matrix[0].size
    initial_memo = dynamic_setup(matrix, size)
    memo = dynamic_solve(matrix, initial_memo, size)
    result = find_min_cost(matrix, memo, size)
    optimal_tour = find_optimal_tour(matrix, memo, size)

    return (result, optimal_tour)
