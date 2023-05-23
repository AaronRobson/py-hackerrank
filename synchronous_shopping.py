# https://www.hackerrank.com/challenges/synchronous-shopping/problem

from typing import Dict, Optional, Tuple, Set, NamedTuple
from sys import maxsize

Cache = Dict[Set[int], int]


def shop(n, k, centers, roads):
    # cats_count = 2
    # cats = parse_cats(cats_count)

    vertices = parse_vertices(n)
    starting_vertex = vertices[0]
    finishing_vertex = vertices[-1]

    fishes = parse_fishes(k)

    centers = parse_centers(centers)
    roads = parse_roads(roads)

    cache: Cache = {}

    cache.update(
        {
            frozenset({starting_vertex, a}): cost
            for a, cost in dijkstra(
                vertices=vertices,
                edges=roads,
                from_=starting_vertex,
            ).items()
        }
    )

    fishes = set(fishes) - centers[starting_vertex] - centers[finishing_vertex]
    if not fishes:
        return cache[frozenset({starting_vertex, finishing_vertex})]

    # todo have the cats explore different combinations of other centers for fishes we need
    return 0


def _one_to_n(n: int) -> Tuple[int, ...]:
    return tuple(range(1, n + 1))


parse_cats = _one_to_n
parse_vertices = _one_to_n
parse_fishes = _one_to_n


def parse_centers(centers):
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


def dijkstra(vertices: Tuple[int], edges: Tuple[Road], from_: int) -> Dict[int, int]:
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


def _find_direct_roads(*, edges: Tuple[Road], from_: int) -> Dict[int, int]:
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
