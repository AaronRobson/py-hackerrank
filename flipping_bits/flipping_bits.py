#!/bin/python3

import os

MIN_UINT_32: int = 0
MAX_UINT_32: int = 2**32 - 1


def flipping_bits(n: int) -> int:
    if not MIN_UINT_32 <= n <= MAX_UINT_32:
        raise ValueError('Value is out of bounds')
    return MAX_UINT_32 ^ n


def main() -> None:
    with open(os.environ['OUTPUT_PATH'], 'w', encoding='utf-8') as fptr:
        q = int(input().strip())
        for _ in range(q):
            n = int(input().strip())
            result = flipping_bits(n)
            fptr.write(str(result) + '\n')


if __name__ == '__main__':
    main()
