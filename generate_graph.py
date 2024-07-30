from typing import Generator


def graphviz_info(*, centers: list[str], roads: list[list[int]], indent: str = ' ' * 2) -> Generator[str, None, None]:
    yield 'strict graph {'
    yield f'{indent}rankdir=LR;'
    yield f'{indent}overlap=false;'
    yield f'{indent}node [shape=box]'
    for i, center in enumerate(centers, start=1):
        foods = center.split()[1:]
        attributes = []
        if foods:
            attributes.append(f'label="{i} ({", ".join(foods)})"')
        if i in (1, len(centers)):
            attributes.append('shape="oval"')
        attribute_str = f' [{", ".join(attributes)}]' if attributes else ''
        yield f'{indent}{i}{attribute_str};'
    for from_, to_, cost in roads:
        yield f'{indent}{from_} -- {to_} [label={cost}];'
    yield '}'


def main() -> None:
    first_multiple_input = input().rstrip().split()

    center_count = int(first_multiple_input[0])

    road_count = int(first_multiple_input[1])

    fish_count = int(first_multiple_input[2])  # noqa: F841

    centers = []

    for _ in range(center_count):
        centers_item = input()
        centers.append(centers_item)

    roads = []

    for _ in range(road_count):
        roads.append(list(map(int, input().rstrip().split())))

    for line in graphviz_info(
        centers=centers,
        roads=roads,
    ):
        print(line)


if __name__ == '__main__':
    main()
