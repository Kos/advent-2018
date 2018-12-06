import pytest
from dataclasses import dataclass
from collections import Counter, defaultdict
from datetime import datetime
from typing import Optional
from enum import Enum


class Action(Enum):
    begin = 0
    sleep = 1
    wake = 2


@dataclass
class Event:
    timestamp: datetime
    guard_id: Optional[int]
    action: Action


@pytest.fixture
def data():
    with open("day4.txt") as f:
        return map(read_line, f.readlines())


@pytest.fixture
def sorted_data(data):
    return sorted(data, key=lambda x: x.timestamp)


def read_line(line):
    date_string = line.split("]")[0].lstrip("[")
    timestamp = datetime.strptime(date_string, "%Y-%m-%d %H:%M")
    if "begins shift" in line:
        action = Action.begin
        guard_id = int(line.split("#")[1].split(" ")[0])
    elif "falls asleep" in line:
        action = Action.sleep
        guard_id = None
    elif "wakes up" in line:
        action = Action.wake
        guard_id = None
    else:
        raise ValueError("Cannot read line: " + line)
    return Event(timestamp=timestamp, action=action, guard_id=guard_id)


def test_data(data):
    assert list(data)[0] == Event(datetime(1518, 11, 22, 00, 49), None, Action.wake)


def get_guard_sleep_ranges(data):
    times = defaultdict(list)
    current_guard = None
    current_sleep_minute = None
    for event in data:
        if event.action == Action.begin:
            assert current_sleep_minute is None, "Guards don't change when asleep"
            current_guard = event.guard_id
        elif event.action == Action.sleep:
            assert current_guard is not None
            current_sleep_minute = event.timestamp.minute
        elif event.action == Action.wake:
            assert current_guard is not None
            assert (
                current_sleep_minute is not None
            ), "Guards must sleep before waking up"
            wake_minute = event.timestamp.minute
            times[current_guard].append((current_sleep_minute, wake_minute))
            current_sleep_minute = None
    return times


def get_sleepiest_guard(ranges):
    def total_time_slept(guard_id):
        return sum(b - a for a, b in ranges[guard_id])

    return max(ranges.keys(), key=total_time_slept)


def get_best_minute(tuples):
    minutes = Counter()
    for a, b in tuples:
        minutes.update(range(a, b))
    return next(iter(minutes.most_common()))[0]


def test_get_best_minute():
    ts = [(0, 5), (2, 5), (4, 8)]
    assert get_best_minute(ts) == 4


def test_get_sleepiest_guard(sorted_data):
    ranges = get_guard_sleep_ranges(sorted_data)
    guard_id = get_sleepiest_guard(ranges)
    best_minute = get_best_minute(ranges[guard_id])
    assert 3557 == guard_id
    assert 30 == best_minute


def get_most_regular_guard(ranges):
    hits = Counter()
    for guard_id, pairs in ranges.items():
        for a, b in pairs:
            for minute in range(a, b):
                hits[guard_id, minute] += 1
    (guard_id, minute), _ = next(iter(hits.most_common()))
    return guard_id, minute


def test_get_most_regular_guard(sorted_data):
    ranges = get_guard_sleep_ranges(sorted_data)
    guard_id, minute = get_most_regular_guard(ranges)
    assert 269 == guard_id
    assert 39 == minute
