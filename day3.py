import pytest
from dataclasses import dataclass
from itertools import product
from collections import Counter, defaultdict
import re


@dataclass
class Claim:
    id: int
    x: int
    y: int
    w: int
    h: int

    def coordinates(self):
        return product(range(self.x, self.x + self.w), range(self.y, self.y + self.h))


@pytest.fixture
def data():
    pattern = re.compile(r"#(?P<id>\d+) @ (?P<x>\d+),(?P<y>\d+): (?P<w>\d+)x(?P<h>\d+)")
    with open("day3.txt") as f:
        return (
            Claim(**{k: int(v) for k, v in pattern.match(line).groupdict().items()})
            for line in f.readlines()
        )


def test_data(data):
    assert list(data)[0] == Claim(1, 755, 138, 26, 19)


def get_overlap_area(data):
    claims = Counter()
    for claim in data:
        claims.update(claim.coordinates())
    return sum(1 for value in claims.values() if value > 1)


def get_good_claims(data):
    claims = defaultdict(set)
    possible_good_claims = set()
    for claim in data:
        possible_good_claims.add(claim.id)
        for coord in claim.coordinates():
            claims[coord].add(claim.id)
            if len(claims[coord]) > 1:
                possible_good_claims = possible_good_claims - claims[coord]
    return list(possible_good_claims)


def test_get_overlap_area(data):
    assert 103482 == get_overlap_area(data)


def test_get_good_claims(data):
    good_claims = get_good_claims(data)
    assert len(good_claims) == 1
    assert 686 == good_claims[0]
