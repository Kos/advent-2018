import pytest
import string
import re
import random
from collections import deque


def reacts(a: str, b: str):
    return a != b and a.lower() == b.lower()


@pytest.mark.parametrize(
    "a,b,expected",
    [
        ("a", "a", False),
        ("a", "A", True),
        ("A", "a", True),
        ("A", "A", False),
        ("A", "b", False),
        ("B", "b", True),
    ],
)
def test_reacts(a, b, expected):
    assert reacts(a, b) == expected


@pytest.fixture
def data():
    with open("day5.txt") as f:
        return f.read().strip()


def test_data_sanitycheck(data):
    assert data.startswith("hHsSm")
    assert data.endswith("JZCcJjI")
    assert data.isalpha()


def pytest_generate_tests(metafunc):
    if "random_data" in metafunc.fixturenames:
        metafunc.parametrize("random_data", gen_random_data())


def gen_random_data():
    n_tests = 5
    test_size = 10000

    rng = random.Random(89245879)
    for i in range(n_tests):
        expected = "".join(rng.choice(string.ascii_lowercase) for _ in range(5))
        data = list(expected)
        for i in range(test_size):
            point = rng.randint(0, len(data))
            letter = rng.choice(string.ascii_lowercase)
            bit = rng.choice([[letter, letter.upper()], [letter.upper(), letter]])
            data[point:point] = bit

        data = "".join(data)
        yield data, expected


def is_stable(polymer: str):
    for i in range(len(polymer) - 1):
        a = polymer[i]
        b = polymer[i + 1]
        if reacts(a, b):
            return False
    return True


def get_reacted_polymer(data):
    stack = deque()
    for unit in data:
        if stack and reacts(unit, stack[-1]):
            stack.pop()
        else:
            stack.append(unit)
    assert is_stable(stack)
    return "".join(map(str, stack))


def get_reacted_polymer_stupid(data):
    pattern = re.compile(
        "|".join(
            [
                *(letter + letter.upper() for letter in string.ascii_lowercase),
                *(letter + letter.lower() for letter in string.ascii_uppercase),
            ]
        )
    )
    while not is_stable(data):
        data = pattern.sub("", data)
    return data


@pytest.fixture(params=[get_reacted_polymer, get_reacted_polymer_stupid])
def impl(request):
    return request.param


@pytest.mark.parametrize(
    "data,expected",
    [
        ("aaaaa", "aaaaa"),
        ("aaaaaAAAAA", ""),
        ("aAaAa", "a"),
        ("abBA", ""),
        ("aabAAB", "aabAAB"),
        ("dabAcCaCBAcCcaDA", "dabCBAcaDA"),
    ],
)
def test_get_reacted_polymer(impl, data, expected):
    assert impl(data) == expected


def test_get_reacted_polymer_random(impl, random_data):
    data, expected = random_data
    assert impl(data) == expected


def test_get_reacted_polymer_solution(impl, data):
    reacted = impl(data)
    assert 11814 == len(reacted)


def improved_polymers(polymer):
    for letter in string.ascii_lowercase:
        yield "".join(x for x in polymer if x.lower() != letter)


def test_improved_polymers():
    improved = list(improved_polymers("aAbBzZbBa"))
    assert improved[0] == "bBzZbB"
    assert improved[1] == "aAzZa"
    assert improved[-1] == "aAbBbBa"


def get_shortest_improved_polymer(polymer):
    return min(improved_polymers(polymer), key=lambda p: len(get_reacted_polymer(p)))


def test_get_shortest_improved_polymer(input, expected_output):
    assert get_shortest_improved_polymer(input) == expected_output


def test_get_shortest_improved_polymer_solution(data):
    best = get_shortest_improved_polymer(data)
    assert 4282 == len(get_reacted_polymer(best))
