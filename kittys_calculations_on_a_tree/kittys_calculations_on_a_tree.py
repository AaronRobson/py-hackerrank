#!/bin/python3

'''https://www.hackerrank.com/challenges/kittys-calculations-on-a-tree/problem
'''

import itertools
from typing import NamedTuple, Optional


def main() -> None:
    parsed = parse()
    outputs = calc(parsed)
    for output in outputs:
        print(output)


class Edge(NamedTuple):
    a: int
    b: int


Edges = list[Edge]


Sets = list[set]


class Data(NamedTuple):
    n: int
    q: int
    edges: Edges
    sets: Sets


Pair = tuple[int, int]


def parse() -> Data:
    n, q = map(int, input().strip().split())
    if not 1 <= n <= 2 * 10 ** 5:
        raise ValueError("'n' out of bounds")

    edges: list[Edge] = []
    for _ in range(n - 1):
        a, b = map(int, input().strip().split())
        if not 1 <= a <= n:
            raise ValueError("'a' out of bounds")
        if not 1 <= b <= n:
            raise ValueError("'b' out of bounds")
        edges.append(Edge(a=a, b=b))

    if not 1 <= q <= 10 ** 5:
        raise ValueError("'q' is out of bounds")

    sets: Sets = []
    for _ in range(q):
        k = int(input().strip())
        if not 1 <= k <= 10 ** 5:
            raise ValueError("'k' is out of bounds")
        set_elements = list(map(int, input().strip().split()))
        if k != len(set_elements):
            raise ValueError("'k' should equal the number of elements")
        current_set = set(set_elements)
        if len(set_elements) != len(current_set):
            raise ValueError('all sets should contain distinct elements')
        sets.append(current_set)

    return Data(
        n=n,
        q=q,
        edges=edges,
        sets=sets,
    )


def calc(d: Data) -> list[int]:
    output = []
    cache: dict[Pair, int] = {}
    for s in d.sets:
        sub_total = 0
        for pair in ordered_pairs(s):
            a, b = list(sorted(pair))
            sub_total += a * b * dist(a, b, d=d, cache=cache)
        output.append(sub_total % ((10 ** 9) + 7))
    return output


def ordered_pairs(s: set) -> list[Pair]:
    ordered_list = list(sorted(s))
    return list(itertools.combinations(ordered_list, r=2))


def dist(a: int, b: int, d: Data, cache: Optional[dict[Pair, int]] = None) -> int:
    if cache is None:
        cache = {}
    if not cache:
        for edge in d.edges:
            cache[edge] = 1
            a, b = edge
            cache[(b, a)] = 1
    if (a, b) in cache:
        return cache[(a, b)]
    output = 1 + min(
        itertools.chain(
            (
                dist(y, b, d, cache)
                for (x, y) in d.edges
                if x == a
            ),
            (
                dist(x, b, d, cache)
                for (x, y) in d.edges
                if y == a
            ),
        )
    )

    cache[(a, b)] = output
    cache[(b, a)] = output
    return output


if __name__ == '__main__':
    main()
