from collections import Counter
import pytest


def get_checksum(lines):
    sum_a, sum_b = 0, 0
    for line in lines:
        counter = Counter(line)
        sum_a += any(value == 2 for value in counter.values())
        sum_b += any(value == 3 for value in counter.values())
    return sum_a * sum_b


def find_the_thing(data):
    for k in range(len(data)):
        c = Counter(transmute(line, k) for line in data)
        for a, b in c.items():
            if b > 1:
                return a.strip()


def transmute(s, n):
    return s[:n] + s[n + 1 :]


def test_get_checksum(data):
    assert 4940 == get_checksum(data)


def test_find_the_thing(data):
    assert "wrziyfdmlumeqvaatbiosngkc" == find_the_thing(data)


@pytest.fixture
def data():
    with open("day2.txt") as f:
        return f.readlines()
