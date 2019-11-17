import src.tools as tools
import pytest


def test_dist():
    assert tools.dist((9, 6), (6, 2)) == 5
    assert tools.dist((-9, 6), (-6, 2)) == 5
    with pytest.raises(TypeError):
        tools.dist()
        tools.dist(3)
        tools.dist([], [])
        tools.dist([1, None], [1, 1])


def test_weighted_edges():
    assert tools.weighted_edges([[1, 2]]) == []
    assert tools.weighted_edges([(9, 6), (6, 2)]) == [(0, 1, 5.0)]
    with pytest.raises(TypeError):
        tools.weighted_edges()
        tools.weighted_edges(3)
        tools.weighted_edges([[], []])
        tools.weighted_edges([1, None], [1, 1])