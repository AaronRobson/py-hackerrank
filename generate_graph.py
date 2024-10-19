from typing import Generator

from synchronous_shopping import input_data


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
    data = input_data(input)

    for line in graphviz_info(
        centers=data['centers'],
        roads=data['roads'],
    ):
        print(line)


if __name__ == '__main__':
    main()
