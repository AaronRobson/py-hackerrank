#!/bin/python3

from itertools import islice
import os


def nth(iterable, n, default=None):
    "Returns the nth item or a default value."
    return next(islice(iterable, n, None), default)


def fibonacci_modified_sequence(t1, t2):
    while True:
        yield t1
        t1, t2 = t2, t1 + t2 ** 2


def fibonacci_modified(t1, t2, n):
    return nth(fibonacci_modified_sequence(t1, t2), n - 1)


def main() -> None:
    with open(os.environ['OUTPUT_PATH'], 'w') as fptr:
        first_multiple_input = input().rstrip().split()

        t1 = int(first_multiple_input[0])
        t2 = int(first_multiple_input[1])
        n = int(first_multiple_input[2])

        result = fibonacci_modified(t1, t2, n)
        fptr.write(str(result) + '\n')


if __name__ == '__main__':
    main()
