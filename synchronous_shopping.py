#!/bin/python3

'''https://www.hackerrank.com/challenges/synchronous-shopping/problem
'''

import os
from typing import Dict, List, Optional, Tuple, Set, FrozenSet, NamedTuple, Sequence
from sys import maxsize
from itertools import permutations


def _pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


try:
    # Available in python3.11+
    from itertools import pairwise  # type: ignore[attr-defined]
except ImportError:
    from itertools import tee
    pairwise = _pairwise


Cache = Dict[FrozenSet[int], int]
Center = int
Centers = Dict[Center, Set[int]]


def shop(n: int, k: int, centers, roads) -> int:
    cats_count = 2
    # cats = parse_cats(cats_count)

    vertices = parse_vertices(n)
    starting_vertex = vertices[0]
    finishing_vertex = vertices[-1]

    fishes = parse_fishes(k)

    centers = parse_centers(centers)
    roads = parse_roads(roads)

    cache: Cache = {}

    for a, cost in dijkstra(
                vertices=vertices,
                edges=roads,
                from_=starting_vertex,
            ).items():
        if starting_vertex == a:
            continue
        cache[frozenset([starting_vertex, a])] = cost

    fishes = fishes - centers[starting_vertex] - centers[finishing_vertex]
    if not fishes:
        return cache[frozenset([starting_vertex, finishing_vertex])]

    centers_with_fish_we_need = find_centers_with_fishes_we_need(centers=centers, fishes_we_need=fishes)

    all_permutations_of_centers = permutations(centers_with_fish_we_need.items())
    all_permutations_of_centers_with_early_exits = (
        stop_early_when_all_fish_are_found(
            centers_permutation=centers_permutation,
            fishes_we_need=fishes)
        for centers_permutation in all_permutations_of_centers)

    potential_routes: Sequence[Tuple[Tuple[int, ...], Tuple[int, ...]]] = (
        (
            (starting_vertex,) + cat_1_route + (finishing_vertex,),
            (starting_vertex,) + cat_2_route + (finishing_vertex,),
        )
        for permutation in all_permutations_of_centers_with_early_exits
        for cat_1_route, cat_2_route in all_splits_in_two(permutation)
    )
    current_min_cost = maxsize
    for potential_route in potential_routes:
        cat_route_costs: List[int] = []
        if len(potential_route) != cats_count:
            raise ValueError(f'Expected len(potential_route)=={cats_count!r} but was {len(potential_route)!r}')
        for cat_route in potential_route:
            cat_route_cost = 0
            for from_, to_ in pairwise(cat_route):
                current_frozen_set = frozenset([from_, to_])
                if current_frozen_set not in cache:
                    for a, cost in dijkstra(
                                vertices=vertices,
                                edges=roads,
                                from_=from_,
                            ).items():
                        if from_ == a:
                            continue
                        cache[current_frozen_set] = cost
                cat_route_cost += cache[current_frozen_set]
            cat_route_costs.append(cat_route_cost)
        current_min_cost = min(current_min_cost, max(cat_route_costs))
    return current_min_cost


def _one_to_n(n: int) -> Tuple[int, ...]:
    return tuple(range(1, n + 1))


def _one_to_n_set(n: int) -> Set[int]:
    return set(_one_to_n(n))


parse_cats = _one_to_n
parse_vertices = _one_to_n
parse_fishes = _one_to_n_set


def parse_centers(centers) -> Centers:
    return {
        i: set(map(int, center.split()[1:]))
        for i, center in enumerate(centers, start=1)
    }


class Road(NamedTuple):
    route: Set[int]  # Expected to have a length of exactly 2.
    cost: int  # Expected to not be negative.


Route = Road

# class RoadFrom(NamedTuple):
#     to_: int
#     cost: int  # Expected to not be negative.


def parse_roads(roads) -> Tuple[Road, ...]:
    return tuple(
        Road(route={road[0], road[1]}, cost=road[2])
        for road in roads)


def dijkstra(vertices: Tuple[int, ...], edges: Tuple[Road, ...], from_: int) -> Dict[int, int]:
    '''https://www.youtube.com/watch?v=EFg3u_E6eHU
    '''
    set_latest = {vertex: Node() for vertex in vertices}
    set_latest[from_].latest_cost = 0
    node_in_progress: Optional[int] = from_

    while node_in_progress is not None:
        for to, cost in _find_direct_roads(edges=edges, from_=node_in_progress).items():
            if set_latest[to].explored:
                continue
            this_cost = set_latest[node_in_progress].latest_cost + cost
            if set_latest[to].latest_cost > this_cost:
                set_latest[to].latest_cost = this_cost

        set_latest[node_in_progress].explored = True
        node_in_progress = _find_new_node_in_progress(set_latest)

    return {
        key: value.latest_cost
        for key, value in set_latest.items()
    }


class Node():
    def __init__(self, *, latest_cost: int = maxsize, explored: bool = False):
        self.latest_cost = latest_cost
        self.explored = explored

    def __repr__(self):
        items = []
        if self.latest_cost != maxsize:
            items.append(f'latest_cost={self.latest_cost!r}')
        if self.explored:
            items.append(f'explored={self.explored!r}')
        return f'{self.__class__.__name__}({", ".join(items)})'


def _find_direct_roads(*, edges: Tuple[Road, ...], from_: int) -> Dict[int, int]:
    output = {}
    for edge in edges:
        if from_ in edge.route:
            to_ = list(edge.route - {from_})[0]
            output[to_] = edge.cost
    return output


def _find_new_node_in_progress(set_latest) -> Optional[int]:
    unexplored = [(key, value) for key, value in set_latest.items() if not value.explored]
    if not unexplored:
        return None
    return min(unexplored, key=lambda item: item[1].latest_cost)[0]


def find_centers_with_fishes_we_need(*, centers: Centers, fishes_we_need: Set[int]) -> Centers:
    return {
        center: fishes_of_center
        for center, fishes_of_center in centers.items()
        if fishes_we_need & fishes_of_center
    }


def stop_early_when_all_fish_are_found(*, centers_permutation: Tuple[Tuple[int, Set[int]], ...], fishes_we_need: Set[int]) -> Sequence[int]:
    fishes_we_have: Set[int] = set()
    for center, fishes_of_center in centers_permutation:
        if not bool(fishes_we_need - fishes_we_have):
            break
        yield center
        fishes_we_have |= fishes_of_center


def all_splits_in_two(centers: Sequence[int]) -> Sequence[Tuple[Tuple[int, ...], Tuple[int, ...]]]:
    centers = tuple(centers)
    for i in range(0, len(centers) + 1):
        yield (
            centers[:i],
            centers[i:],
        )


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])

    m = int(first_multiple_input[1])

    k = int(first_multiple_input[2])

    centers = []

    for _ in range(n):
        centers_item = input()
        centers.append(centers_item)

    roads = []

    for _ in range(m):
        roads.append(list(map(int, input().rstrip().split())))

    res = shop(n, k, centers, roads)

    fptr.write(str(res) + '\n')

    fptr.close()
