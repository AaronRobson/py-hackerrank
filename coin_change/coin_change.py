#!/bin/python3

import os


def get_ways(n, c):
    if n == 0:
        return 1
    if not c:
        return 0
    ways_including_first_coin = get_ways(n - c[0], c) if c[0] <= n else 0
    ways_without_first_coin = get_ways(n, c[1:])
    return ways_including_first_coin + ways_without_first_coin


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
