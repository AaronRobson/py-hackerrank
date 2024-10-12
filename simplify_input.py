import argparse


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='Graph representation simplifier',
    )
    parser.add_argument(
        '--steps',
        type=str,
        nargs='+',
        dest='steps',
    )
    return parser


def input_data() -> dict:
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

    return {
        'center_count': center_count,
        'road_count': road_count,
        'fish_count': fish_count,
        'centers': centers,
        'roads': roads,
    }


def output_data(
    *,
    center_count,
    road_count,
    fish_count,
    centers,
    roads,
) -> None:
    print(f'{center_count} {road_count} {fish_count}')
    for center in centers:
        print(center)
    for road in roads:
        print(' '.join(map(str, road)))
    print()


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
            # skip removing the start or fish centers
            if center in (1, center_count):
                continue
            # skip removing center with fish
            if centers[center - 1] != '0':
                continue
            # skip removing centers that aren't dead ends
            if len(links) >= 2:
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


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()

    data = input_data()
    for step in args.steps:
        if step == 'id':
            data = simplify_id(**data)
        elif step == 'fish':
            data = simplify_fish(**data)
        elif step == 'deadends':
            data = simplify_deadends(**data)
        else:
            raise ValueError(f'step {step!r} is not recognised')
    output_data(**data)


if __name__ == '__main__':
    main()
