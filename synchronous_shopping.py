#!/bin/python3

'''https://www.hackerrank.com/challenges/synchronous-shopping/problem
'''

from collections import defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from functools import partial
from operator import attrgetter
import os
from typing import Any, Optional, NamedTuple
try:
    # Requires python3.11+
    # https://docs.python.org/3.11/library/typing.html#typing.Self
    from typing import Self  # type: ignore[attr-defined]
except ImportError:
    from typing import TypeVar
    # If other classes require this then this needs to change.
    Self = TypeVar('Self', bound='Node')  # type: ignore[misc]
from sys import maxsize
from itertools import chain, filterfalse, permutations
import sys


Cache = dict[tuple[int, int], int]
RouteCache = dict[tuple[int, ...], int]

Center = int
Centers = dict[Center, set[int]]


def main() -> None:
    def find_answer(retrieve_next_line_func) -> int:
        first_multiple_input = retrieve_next_line_func().rstrip().split()
        center_count = int(first_multiple_input[0])
        road_count = int(first_multiple_input[1])
        fish_count = int(first_multiple_input[2])
        centers = [
            retrieve_next_line_func()
            for _ in range(center_count)]
        roads = [
            list(map(int, retrieve_next_line_func().rstrip().split()))
            for _ in range(road_count)]
        return shop(
            fish_count=fish_count,
            centers=centers,
            roads=roads)

    if len(sys.argv) <= 1:
        res = find_answer(input)
    else:
        filepath = sys.argv[1]
        with open(filepath, 'rt', encoding='utf-8') as fp:
            res = find_answer(fp.readline)

    output_path = os.environ.get('OUTPUT_PATH')
    if output_path:
        with open(os.environ['OUTPUT_PATH'], 'w', encoding='utf-8') as fptr:
            fptr.write(str(res) + '\n')
    else:
        print(res)


def _choose_combinations_of_centers(values: Sequence[Sequence[int]]) -> Iterable[tuple[int, ...]]:
    '''Not all combinations.
    '''
    values = list(values)
    min_value_length = min(map(len, values), default=0)
    has_been_done = set()
    exists = False
    for value in filter(lambda v: len(v) == min_value_length, values):
        for item in value:
            if item in has_been_done:
                continue
            has_been_done.add(item)

            new_values = [
                new_value
                for new_value in values
                if item not in new_value
            ]
            for combination in _choose_combinations_of_centers(new_values):
                exists = True
                yield (item,) + combination
    if not exists:
        # There is only one way to choose no centers.
        yield tuple()


def choose_all_combinations_of_centers(values: Sequence[Sequence[int]]) -> set[tuple[int, ...]]:
    combinations = set(map(frozenset, _choose_combinations_of_centers(values)))

    combinations = set(filterfalse(lambda combination: any(combination > other for other in combinations), combinations))

    return set(chain.from_iterable(map(permutations, combinations)))


class Road(NamedTuple):
    route: set[int]  # Expected to have a length of exactly 2.
    cost: int  # Expected to not be negative.


def _shop(*, vertices: tuple[int, ...], fishes: set[int], centers: Centers, roads: tuple[Road, ...]) -> int:
    # cats_count = 2
    # cats = parse_cats(cats_count)

    starting_vertex = vertices[0]
    finishing_vertex = vertices[-1]

    cache = route_finder(
        vertices=vertices,
        edges=roads,
        important_vertices=tuple({*{1, len(centers)}, *set(vertex for vertex, fishes in centers.items() if fishes)}))

    fishes = fishes - centers[starting_vertex] - centers[finishing_vertex]
    if not fishes:
        return cache[(starting_vertex, finishing_vertex)]

    centers_with_fish_we_need = find_centers_with_fishes_we_need(centers=centers, fishes_we_need=fishes)
    fishes_we_need_to_centers = swap_centers_with_fish_we_need(centers_with_fish_we_need)
    centers_to_choose_from_grouped_by_fishes = set(fishes_we_need_to_centers.values())

    all_permutations_of_centers = choose_all_combinations_of_centers(centers_to_choose_from_grouped_by_fishes)

    route_cache: RouteCache = {}
    potential_route_costs: Iterable[tuple[int, int]] = (
        (
            find_route_costs(cache=cache, route_cache=route_cache, route=(starting_vertex,) + cat_1_route + (finishing_vertex,)),
            find_route_costs(cache=cache, route_cache=route_cache, route=(starting_vertex,) + cat_2_route + (finishing_vertex,)),
        )
        for permutation in all_permutations_of_centers
        for cat_1_route, cat_2_route in all_splits_in_two(permutation)
    )

    return min(map(max, potential_route_costs))


def shop(*, fish_count: int, centers: list[str], roads: list[list[int]]) -> int:
    return _shop(
        vertices=parse_vertices(len(centers)),
        fishes=parse_fishes(fish_count),
        centers=parse_centers(centers),
        roads=parse_roads(roads),
    )


def _one_to_size(size: int) -> tuple[int, ...]:
    return tuple(range(1, size + 1))


def _one_to_size_set(size: int) -> set[int]:
    return set(_one_to_size(size))


parse_cats = _one_to_size
parse_vertices = _one_to_size
parse_fishes = _one_to_size_set


def parse_centers(centers) -> Centers:
    return {
        i: set(map(int, center.split()[1:]))
        for i, center in enumerate(centers, start=1)
    }


def parse_roads(roads) -> tuple[Road, ...]:
    return tuple(
        Road(route={road[0], road[1]}, cost=road[2])
        for road in roads)


def dijkstra(*, vertices: tuple[int, ...], edges: tuple[Road, ...], from_: int) -> dict[int, int]:
    '''https://www.youtube.com/watch?v=EFg3u_E6eHU
    '''
    set_latest = {vertex: Node(vertex=vertex) for vertex in vertices}
    set_latest[from_].latest_cost = 0

    node_in_progress: Optional[int] = from_

    while node_in_progress is not None:
        for to_node, cost in _find_direct_roads(edges=edges, from_=node_in_progress).items():
            if set_latest[to_node].explored:
                continue
            this_cost = set_latest[node_in_progress].latest_cost + cost
            if set_latest[to_node].latest_cost > this_cost:
                set_latest[to_node].latest_cost = this_cost
                set_latest[to_node].previous_node = set_latest[node_in_progress]

        set_latest[node_in_progress].explored = True
        node_in_progress = _find_new_node_in_progress(set_latest)

    # Update cache from each target to all the others in the chain up to (but not including) 'from_'.
    for to_node, value in set_latest.items():
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
                cost = finishing_node.latest_cost - item.latest_cost
                finishing_node.previous_routes_have_been_cached = True

    return {
        key: value.latest_cost
        for key, value in set_latest.items()
    }


def route_finder(vertices: tuple[int, ...], edges: tuple[Road, ...], *, important_vertices: Optional[tuple[int, ...]] = None) -> Cache:
    important_vertices = important_vertices or vertices
    cache: Cache = {}
    for from_ in important_vertices:
        cache.update({
            (from_, to_): cost
            for to_, cost in dijkstra(vertices=vertices, edges=edges, from_=from_).items()
            if from_ != to_ and to_ in important_vertices
        })
    return cache


def find_route_costs(*, cache: Cache, route_cache: RouteCache, route: tuple[int, ...]) -> int:
    try:
        return route_cache[route]
    except KeyError:
        cost = (cache[(route[0], route[1])] + find_route_costs(cache=cache, route_cache=route_cache, route=route[1:])) if len(route) > 1 else 0
        route_cache[route] = cost
        return cost


@dataclass(init=True, repr=True, kw_only=True, slots=True)
class Node():
    vertex: int
    latest_cost: int = maxsize
    explored: bool = False
    previous_node: Optional[Self] = None
    previous_routes_have_been_cached: bool = False


def _find_direct_roads(*, edges: tuple[Road, ...], from_: int) -> dict[int, int]:
    return {
        list(edge.route - {from_})[0]: edge.cost
        for edge in edges
        if from_ in edge.route
    }


def _find_new_node_in_progress(set_latest: dict[int, Node]) -> Optional[int]:
    unexplored = filterfalse(attrgetter('explored'), set_latest.values())
    min_node = min(unexplored, key=attrgetter('latest_cost'), default=None)
    return min_node.vertex if min_node is not None else None


def find_centers_with_fishes_we_need(*, centers: Centers, fishes_we_need: set[int]) -> Centers:
    return {
        center: fishes_of_center
        for center, fishes_of_center in centers.items()
        if not fishes_we_need.isdisjoint(fishes_of_center)
    }


def swap_centers_with_fish_we_need(centers_with_fish_we_need: Centers) -> dict[int, frozenset[int]]:
    fishes_we_need_to_centers = defaultdict(set)
    for center, fishes in centers_with_fish_we_need.items():
        for fish in fishes:
            fishes_we_need_to_centers[fish].add(center)
    return {
        key: frozenset(value)
        for key, value in fishes_we_need_to_centers.items()
    }


def stop_early_when_all_fish_are_found(*, centers_permutation: Iterable[tuple[int, set[int]]], fishes_we_need: set[int]) -> Iterable[int]:
    fishes_we_have: set[int] = set()
    for center, fishes_of_center in centers_permutation:
        if not bool(fishes_we_need - fishes_we_have):
            break
        yield center
        fishes_we_have |= fishes_of_center


def split_at(index: int, values: tuple[Any, ...]) -> tuple[tuple[Any, ...], tuple[Any, ...]]:
    return (
        values[:index],
        values[index:],
    )


def all_splits_in_two(centers: tuple[int, ...]) -> Iterable[tuple[tuple[int, ...], tuple[int, ...]]]:
    length = len(centers)
    func = partial(split_at, values=centers)
    return map(func, range(1 if length > 1 else 0, length))


if __name__ == '__main__':
    main()
