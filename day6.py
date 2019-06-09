import pytest
from scipy.signal import convolve2d
import numpy as np
import string
import re
import random
from typing import Sequence, Tuple
from collections import deque, defaultdict, Counter


@pytest.fixture
def data():
    with open("day6.txt") as f:
        return [tuple(map(int, line.split(", "))) for line in f.readlines()]


def test_data(data):
    assert data[0] == (77, 279)
    assert data[-1] == (117, 129)


def data_shape(data):
    return (max(d[0] for d in data) + 1, max(d[1] for d in data) + 1)


Point = Tuple[int]

BOUNDARY = -1


def neighbours(id, point):
    a, b = point
    return [(id, (a + 1, b)), (id, (a - 1, b)), (id, (a, b - 1)), (id, (a, b + 1))]


def in_shape(coord, shape):
    return all(0 <= value < limit for value, limit in zip(coord, shape))


def gen_voronoi(data):
    regions = np.zeros(data_shape(data))
    print("shape", regions.shape, regions.shape[0] * regions.shape[1])
    boundary: Sequence[Tuple[int, Point]] = deque(enumerate(data, start=1))
    boundary_regions = set()
    region_sizes = defaultdict(int)
    iterations = 0
    while boundary:
        print(iterations, len(boundary))
        iterations += 1
        if iterations == 1000:
            raise ValueError("Didn't stop after 1000 iterations")

        next_boundary = deque()
        growth = np.zeros(regions.shape)
        for id, coord in boundary:
            if not in_shape(coord, regions.shape):
                boundary_regions.add(id)
                continue
            if regions[coord]:
                # Can't grow a region there - already taken
                continue
            next_boundary.extend(neighbours(id, coord))
            if growth[coord]:
                # Two nodes with same distance -
                # grow but mark as boundary
                region_sizes[growth[coord]] -= 1
                growth[coord] = BOUNDARY
            else:
                region_sizes[id] += 1
                growth[coord] = id

        updated_coords = growth != 0
        existing_coords = regions != 0
        if (updated_coords & existing_coords).any():
            assert False, "collision"

        print("growth", growth)
        regions += growth
        boundary = next_boundary

    return max(value for key, value in region_sizes if key not in boundary_regions)


@pytest.mark.skip
def test_voronoi(data):
    assert "?" == gen_voronoi(data)


def get_kernels():
    for a, b in [(0, 1), (2, 1), (1, 0), (1, 2)]:
        kernel = np.zeros((3, 3), dtype=int)
        kernel[a, b] = 1
        yield kernel


def convolve_step(arr):
    steps = [convolve2d(arr, kernel, mode="same") for kernel in get_kernels()]
    new_values = vote(steps)
    return np.where(arr == 0, new_values, arr)


def test_convolve_step():
    a = np.array(
        [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 5, 0, 6, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 7],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ],
        dtype=int,
    )
    b = np.array(
        [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 5, 0, 6, 0, 0],
            [0, 0, 5, 5, 0, 6, 6, 0],
            [0, 0, 0, 5, 0, 6, 0, 7],
            [0, 0, 0, 0, 0, 0, 7, 7],
            [0, 0, 0, 0, 0, 0, 0, 7],
        ],
        dtype=int,
    )
    o = convolve_step(a)
    assert (convolve_step(a) == b).all()


def vote(arrays):
    r = arrays[0]
    for a in arrays[1:]:
        r = np.where(r == 0, a, r)
    for a in arrays[1:]:
        r = np.where((a != 0) & (a != r), 0, r)
    return r


def test_vote():
    a = np.array([0, 1, 0, 2, 0, 3], dtype=int)
    b = np.array([0, 1, 0, 2, 0, 3], dtype=int)
    c = np.array([1, 0, 0, 2, 5, 4], dtype=int)
    o = np.array([1, 1, 0, 2, 5, 0], dtype=int)
    assert (vote([a, b, c]) == o).all()


def convolve_limit(arr):
    new = convolve_step(arr)
    while (arr != new).any():
        arr = new
        new = convolve_step(new)
    return new


from functools import reduce


def get_largest_region_size(array):
    counts = Counter(array.flatten())
    w, h = array.shape
    edge_regions = reduce(
        lambda a, b: a | b,
        [
            {array[i, 0] for i in range(w)},
            {array[i, -1] for i in range(w)},
            {array[0, j] for j in range(h)},
            {array[-1, j] for j in range(h)},
        ],
    )
    return next(
        region_size
        for region_id, region_size in counts.most_common()
        if region_id not in edge_regions
    )


def test_solution(data):
    array = np.zeros(data_shape(data), dtype=int)
    for i, (x, y) in enumerate(data, start=1):
        array[x, y] = i
    result = convolve_limit(array)
    size = get_largest_region_size(result)
    assert 3006 == size

