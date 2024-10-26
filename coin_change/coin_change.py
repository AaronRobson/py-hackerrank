#!/bin/python3

import os


def get_ways(n, c, cache=None):
    if cache is None:
        cache = {}
    c = tuple(c)
    cached_value = cache.get((n, c))
    if cached_value is not None:
        return cached_value
    if n == 0:
        output = 1
        cache[(n, c)] = output
        return output
    if not c:
        output = 0
        cache[(n, c)] = output
        return output
    ways_including_first_coin = get_ways(n - c[0], c, cache) if c[0] <= n else 0
    ways_without_first_coin = get_ways(n, c[1:], cache)
    output = ways_including_first_coin + ways_without_first_coin
    cache[(n, c)] = output
    return output


def main() -> None:
    with open(os.environ['OUTPUT_PATH'], 'w', encoding='utf-8') as fptr:
        first_multiple_input = input().rstrip().split()

        n = int(first_multiple_input[0])

        m = int(first_multiple_input[1])

        c = list(map(int, input().rstrip().split()))

        if m != len(c):
            raise ValueError('length is incorrect')

        # Print the number of ways of making change for 'n' units using coins having the values given by 'c'

        ways = get_ways(n, c)

        fptr.write(str(ways) + '\n')


if __name__ == '__main__':
    main()
