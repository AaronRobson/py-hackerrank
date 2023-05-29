#!/bin/python3

'''https://www.hackerrank.com/challenges/synchronous-shopping/problem
'''

from collections import defaultdict
import os
from typing import Dict, Optional, Tuple, Set, FrozenSet, NamedTuple, Iterable
try:
    # Requires python3.11+
    # https://docs.python.org/3.11/library/typing.html#typing.Self
    from typing import Self  # type: ignore[attr-defined]
except ImportError:
    from typing import TypeVar
    # If other classes require this then this needs to change.
    Self = TypeVar('Self', bound='Node')  # type: ignore[misc]
from sys import maxsize
from itertools import chain, permutations, product, starmap


try:
    # Available in python3.11+
    from itertools import pairwise  # type: ignore[attr-defined]
except ImportError:
    from itertools import tee

    def pairwise(iterable):
        '''From: https://docs.python.org/3/library/itertools.html#itertools.pairwise
        '''
        # pairwise('ABCDEFG') --> AB BC CD DE EF FG
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)


Cache = Dict[FrozenSet[int], int]
Center = int
Centers = Dict[Center, Set[int]]


def shop(n: int, k: int, centers, roads) -> int:
    # cats_count = 2
    # cats = parse_cats(cats_count)

    vertices = parse_vertices(n)
    starting_vertex = vertices[0]
    finishing_vertex = vertices[-1]

    fishes = parse_fishes(k)

    centers = parse_centers(centers)
    roads = parse_roads(roads)

    rf = RouteFinder(
        vertices=vertices,
        edges=roads)

    fishes = fishes - centers[starting_vertex] - centers[finishing_vertex]
    if not fishes:
        return rf.find_route_cost(starting_vertex, finishing_vertex)

    centers_with_fish_we_need = find_centers_with_fishes_we_need(centers=centers, fishes_we_need=fishes)
    fishes_we_need_to_centers = swap_centers_with_fish_we_need(centers_with_fish_we_need)
    centers_to_choose_from_grouped_by_fishes = set(fishes_we_need_to_centers.values())

    all_products_with_duplicates = product(*centers_to_choose_from_grouped_by_fishes)
    all_products = (
        tuple(dict.fromkeys(permutation))
        for permutation in all_products_with_duplicates
    )
    all_permutations_of_centers: Iterable[Tuple[int, ...]] = chain.from_iterable(map(permutations, all_products))

    potential_routes: Iterable[Tuple[Tuple[int, ...], Tuple[int, ...]]] = (
        (
            (starting_vertex,) + cat_1_route + (finishing_vertex,),
            (starting_vertex,) + cat_2_route + (finishing_vertex,),
        )
        for permutation in all_permutations_of_centers
        for cat_1_route, cat_2_route in all_splits_in_two(permutation)
        if cat_1_route < cat_2_route
    )

    def find_potential_route_cost(potential_route: Tuple[Tuple[int, ...], Tuple[int, ...]]) -> int:
        return max(map(rf.find_route_costs, potential_route))

    return min(map(find_potential_route_cost, potential_routes))


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
    '''This will not be able to use the cache on subsequent calls.
    '''
    return RouteFinder(
        vertices=vertices,
        edges=edges,
    ).dijkstra(from_=from_)


class RouteFinder():
    def __init__(self, vertices: Tuple[int, ...], edges: Tuple[Road, ...]):
        self.vertices = vertices
        self.edges = edges
        self.reset_cache()

    def reset_cache(self):
        self.cache: Cache = {}

    def find_route_cost(self, from_: int, to: int) -> int:
        current_cache_value = self.cache.get(frozenset((from_, to)), None)
        if current_cache_value is not None:
            return current_cache_value
        return self.dijkstra(from_=from_)[to]

    def find_route_costs(self, cat_route: Iterable[int]) -> int:
        return sum(
            starmap(
                self.find_route_cost,
                pairwise(cat_route)))

    def dijkstra(self, *, from_: int) -> Dict[int, int]:
        '''https://www.youtube.com/watch?v=EFg3u_E6eHU
        '''
        set_latest = {vertex: Node(vertex=vertex) for vertex in self.vertices}
        set_latest[from_].latest_cost = 0

        node_in_progress: Optional[int] = from_

        while node_in_progress is not None:
            for to, cost in _find_direct_roads(edges=self.edges, from_=node_in_progress).items():
                if set_latest[to].explored:
                    continue
                this_cost = set_latest[node_in_progress].latest_cost + cost
                if set_latest[to].latest_cost > this_cost:
                    set_latest[to].latest_cost = this_cost
                    set_latest[to].previous_node = set_latest[node_in_progress]

            set_latest[node_in_progress].explored = True
            node_in_progress = _find_new_node_in_progress(set_latest)

        # Update cache - 'from_' to every other node.
        self.cache.update({
            frozenset((from_, to)): value.latest_cost
            for to, value in set_latest.items()
        })

        # Update cache from each target to all the others in the chain up to (but not including) 'from_'.
        for to, value in set_latest.items():
            if value.previous_routes_have_been_cached:
                continue
            node = value
            route = []
            while node.previous_node is not None:
                route.append(node)
                node = node.previous_node
            while route:
                finishing_node = route[0]
                if finishing_node.previous_routes_have_been_cached:
                    break
                route = route[1:]
                for item in route:
                    self.cache[frozenset((finishing_node.vertex, item.vertex))] = finishing_node.latest_cost - item.latest_cost
                    finishing_node.previous_routes_have_been_cached = True

        return {
            key: value.latest_cost
            for key, value in set_latest.items()
        }


class Node():
    __slots__ = (
        'vertex',
        'latest_cost',
        'explored',
        'previous_node',
        'previous_routes_have_been_cached',
    )

    def __init__(
            self,
            *,
            vertex: int = 0,
            latest_cost: int = maxsize,
            explored: bool = False,
            previous_node: Optional[Self] = None,
            previous_routes_have_been_cached: bool = False):
        self.vertex = vertex
        self.latest_cost = latest_cost
        self.explored = explored
        self.previous_node = previous_node
        self.previous_routes_have_been_cached = previous_routes_have_been_cached

    def __repr__(self):
        items = []
        if self.vertex != 0:
            items.append(f'vertex={self.vertex!r}')
        if self.latest_cost != maxsize:
            items.append(f'latest_cost={self.latest_cost!r}')
        if self.explored:
            items.append(f'explored={self.explored!r}')
        if self.previous_node is not None:
            items.append(f'previous_node_={self.previous_node!r}')
        if self.previous_routes_have_been_cached:
            items.append(f'previous_routes_have_been_cached={self.previous_routes_have_been_cached!r}')
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
        if not fishes_we_need.isdisjoint(fishes_of_center)
    }


def swap_centers_with_fish_we_need(centers_with_fish_we_need: Centers) -> Dict[int, FrozenSet[int]]:
    fishes_we_need_to_centers = defaultdict(set)
    for center, fishes in centers_with_fish_we_need.items():
        for fish in fishes:
            fishes_we_need_to_centers[fish].add(center)
    return {
        key: frozenset(value)
        for key, value in fishes_we_need_to_centers.items()
    }


def stop_early_when_all_fish_are_found(*, centers_permutation: Iterable[Tuple[int, Set[int]]], fishes_we_need: Set[int]) -> Iterable[int]:
    fishes_we_have: Set[int] = set()
    for center, fishes_of_center in centers_permutation:
        if not bool(fishes_we_need - fishes_we_have):
            break
        yield center
        fishes_we_have |= fishes_of_center


def all_splits_in_two(centers: Iterable[int]) -> Iterable[Tuple[Tuple[int, ...], Tuple[int, ...]]]:
    centers_all = tuple(centers)
    for i in range(0, len(centers_all) + 1):
        yield (
            centers_all[:i],
            centers_all[i:],
        )


if __name__ == '__main__':
    with open(os.environ['OUTPUT_PATH'], 'w') as fptr:
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
