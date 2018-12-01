from itertools import cycle


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


if __name__ == '__main__':
    with open('day1.txt') as f:
        data = list(map(int, f.readlines()))

    print("Resulting frequency: ", get_resulting_frequency(data))
    print("First frequency reached twice: ", get_first_frequency_reached_twice(data))
