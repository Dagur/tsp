import src.hameltonian as ht
import pytest
import numpy


def test_flatten():
    assert ht.flatten((123, 3)) == (123, [3])
    assert ht.flatten(((((((123, 3), 4), 5), 6), 7), 8)) == (123, [8, 7, 6, 5, 4, 3])
    assert ht.flatten((None, 4)) == (None, [4])
    with pytest.raises(ValueError):
        ht.flatten([])
    with pytest.raises(TypeError):
        ht.flatten(None)
    with pytest.raises(ValueError):
        ht.flatten([None])
    with pytest.raises(ValueError):
        ht.flatten((34,))


def test_bits():
    assert list(ht.bits(0)) == []
    assert list(ht.bits(1)) == [1]
    assert next(ht.bits(-1)) == 1
    assert list(ht.bits(None)) == []


def test_index():
    assert ht.index(1) == 0
    assert ht.index(2) == 1
    assert ht.index(3) == 1
    assert ht.index(4) == 2

    with pytest.raises(ValueError):
        ht.index(0)

    with pytest.raises(ValueError):
        ht.index(-1)

