from itertools import cycle
import pytest


def get_resulting_frequency(data):
    return sum(data)


def get_first_frequency_reached_twice(data):
    seen = set()
    count = 0
    for i in cycle(data):
        count += i
        if count in seen:
            return count
        seen.add(count)


def test_get_resulting_frequency(data):
    assert 484 == get_resulting_frequency(data)


def test_get_first_frequency_reached_twice(data):
    assert 367 == get_first_frequency_reached_twice(data)


@pytest.fixture
def data():
    with open("day1.txt") as f:
        return list(map(int, f.readlines()))
