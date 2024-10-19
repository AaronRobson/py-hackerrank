from typing import Optional

from synchronous_shopping import center_to_fish, input_data, output_data


def simplify_id(
    *,
    center_count,
    road_count,
    fish_count,
    centers,
    roads,
):
    return {
        'center_count': center_count,
        'road_count': road_count,
        'fish_count': fish_count,
        'centers': centers,
        'roads': roads,
    }


def simplify_fish(
    *,
    center_count,
    road_count,
    fish_count,
    centers,
    roads,
):
    '''Fish that the start or end points have do not neeed to be included in the graph as they'll be picked up automatically.
    '''
    start_center = centers[0]
    finish_center = centers[-1]
    redundant_fishes = sorted(map(int, set(start_center.split()[1:] + finish_center.split()[1:])), reverse=True)
    fish_count -= len(redundant_fishes)
    # remove redundant fishes
    for i in range(center_count):
        if i in (0, center_count - 1):
            values = []
        else:
            values = [
                int(value)
                for value in centers[i].split()[1:]
                if int(value) not in redundant_fishes
            ]
        if values:
            centers[i] = f'{len(values)} {" ".join(map(str, values))}'
        else:
            centers[i] = '0'
    # shift remaining fish down
    for redundant_fish in redundant_fishes:
        for i in range(center_count):
            pass
            values = [
                int(value)
                for value in centers[i].split()[1:]
            ]
            values = [
                value if value < redundant_fish else (value - 1)
                for value in values
            ]
            if values:
                centers[i] = f'{len(values)} {" ".join(map(str, values))}'
            else:
                centers[i] = '0'

    return {
        'center_count': center_count,
        'road_count': road_count,
        'fish_count': fish_count,
        'centers': centers,
        'roads': roads,
    }


def simplify_deadends(
    *,
    center_count,
    road_count,
    fish_count,
    centers,
    roads,
):
    while True:
        center_links = {i: set() for i in range(1, center_count + 1)}
        for road in roads:
            from_, to_, _ = map(int, road)
            center_links[from_].add(to_)
            center_links[to_].add(from_)
        centers_to_remove = set()
        for center, links in center_links.items():
            # skip removing the start or end centers
            if center in (1, center_count):
                continue
            # skip removing centers that aren't dead ends
            if len(links) >= 2:
                continue
            # skip removing center with fish that the neighbour is missing
            center_fish = center_to_fish(centers[center - 1])
            neighbour_fish = center_to_fish(centers[list(links)[0] - 1])
            if center_fish - neighbour_fish:
                continue
            centers_to_remove.add(center)

        if not centers_to_remove:
            break

        centers = [center for i, center in enumerate(centers, start=1) if i not in centers_to_remove]
        center_count = len(centers)

        # remove centers
        roads = [
            [from_, to_, cost]
            for from_, to_, cost in roads
            if from_ not in centers_to_remove and to_ not in centers_to_remove
        ]
        # shift down road references to centers
        for center_to_remove in sorted(centers_to_remove, reverse=True):
            roads = [
                [
                    from_ if from_ < center_to_remove else (from_ - 1),
                    to_ if to_ < center_to_remove else (to_ - 1),
                    cost,
                ]
                for from_, to_, cost in roads
            ]
        road_count = len(roads)

    return {
        'center_count': center_count,
        'road_count': road_count,
        'fish_count': fish_count,
        'centers': centers,
        'roads': roads,
    }


def simplify_chains(
    *,
    center_count,
    road_count,
    fish_count,
    centers,
    roads,
):
    while True:
        center_links = {i: {} for i in range(1, center_count + 1)}
        for road in roads:
            from_, to_, cost = map(int, road)
            center_links[from_][to_] = cost
            center_links[to_][from_] = cost
        center_to_remove: Optional[int] = None
        for center, links in center_links.items():
            # skip removing the start or end centers
            if center in (1, center_count):
                continue
            # skip removing center with fish
            # TODO consider allowing centers with only fish that both neighbours already have to be removed
            if centers[center - 1] != '0':
                continue
            # skip centers which don't have exactly two roads
            if len(links) != 2:
                continue
            center_to_remove = center
            break
        if center_to_remove is None:
            break
        centers = [center for i, center in enumerate(centers, start=1) if i != center_to_remove]
        center_count = len(centers)
        # remove center
        roads = [
            [from_, to_, cost]
            for from_, to_, cost in roads
            if (from_ != center_to_remove) and (to_ != center_to_remove)
        ]
        # see if a bypass is worthwhile
        from_, to_ = list(links.keys())
        bypass_length = sum(links.values())
        try:
            direct_length = center_links[from_][to_]
        except KeyError:
            direct_length = None
        if direct_length is None:
            # include the bypass road
            roads.append([from_, to_, bypass_length])
        elif direct_length < bypass_length:
            pass  # direct is already quicker
        else:
            # replace direct with quicker bypass
            roads = [
                [from_, to_, cost]
                for from_, to_, cost in roads
                if set([from_, to_]) != set(links.keys())
            ]
            roads.append([from_, to_, bypass_length])
        # shift down road references to centers
        roads = [
            [
                from_ if from_ < center_to_remove else (from_ - 1),
                to_ if to_ < center_to_remove else (to_ - 1),
                cost,
            ]
            for from_, to_, cost in roads
        ]
        road_count = len(roads)
        # break

    return {
        'center_count': center_count,
        'road_count': road_count,
        'fish_count': fish_count,
        'centers': centers,
        'roads': roads,
    }


config = [
    simplify_id,
    simplify_fish,
    simplify_deadends,
    simplify_chains,
]


def simplify(data: dict) -> dict:
    while True:
        diff = False
        for func in config:
            new_data = func(**data)
            if data != new_data:
                diff = True
            data = new_data
        if not diff:
            break
    return data


def main() -> None:
    data = input_data()
    new_data = simplify(data)
    output_data(**new_data)


if __name__ == '__main__':
    main()
