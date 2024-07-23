#!/bin/python3

'''https://www.hackerrank.com/challenges/synchronous-shopping/problem
'''

import os

from synchronous_shopping_lib import shop


def main() -> None:
    with open(os.environ['OUTPUT_PATH'], 'w', encoding='utf-8') as fptr:
        first_multiple_input = input().rstrip().split()

        center_count = int(first_multiple_input[0])

        road_count = int(first_multiple_input[1])

        fish_count = int(first_multiple_input[2])

        centers = []

        for _ in range(center_count):
            centers_item = input()
            centers.append(centers_item)

        roads = []

        for _ in range(road_count):
            roads.append(list(map(int, input().rstrip().split())))

        res = shop(
            center_count=center_count,
            fish_count=fish_count,
            centers=centers,
            roads=roads)

        fptr.write(str(res) + '\n')


if __name__ == '__main__':
    main()
