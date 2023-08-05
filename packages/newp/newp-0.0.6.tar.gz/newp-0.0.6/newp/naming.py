import enum
import string
import typing as t


class Mode(enum.Enum):
    OUTERSPACE = 0
    LETTERS = 1
    NUMBERS = 2


def name_to_components_0(name: str) -> t.List[str]:
    if all([e.isupper() for e in name]):
        name = name.lower()
    slices: t.List[t.Tuple[int, int]] = []
    start = 0
    last_char: str = ""

    in_NUMBERS = False
    for i, e in enumerate(name):
        if e.isupper():
            slices.append((start, i))
            start = i
            in_NUMBERS = False
        elif e in ["-", "_"]:
            if last_char not in ["-", "_"]:
                slices.append((start, i))
                start = i
                in_NUMBERS = False
        elif e.isnumeric():
            if not in_NUMBERS:
                slices.append((start, i))
                start = i
                in_NUMBERS = True
        elif in_NUMBERS:
            slices.append((start, i))
            start = i
            in_NUMBERS = False
        last_char = e

    return [name[s[0] : s[1]] for s in slices]


def name_to_components(name: str) -> t.List[str]:
    if all([e.isupper() for e in name]):
        name = name.lower()
    slices: t.List[t.Tuple[int, int]] = []
    mode = Mode.OUTERSPACE
    start = 0
    for i, e in enumerate(name):
        if e in string.ascii_uppercase:
            if mode != Mode.OUTERSPACE:
                slices.append((start, i))
            start = i
            mode = Mode.LETTERS
        elif e in string.ascii_lowercase:
            if mode != Mode.LETTERS:
                if mode == Mode.NUMBERS:
                    slices.append((start, i))
                start = i
                mode = Mode.LETTERS
        elif e in string.digits:
            if mode != Mode.NUMBERS:
                if mode == Mode.LETTERS:
                    slices.append((start, i))
                start = i
                mode = Mode.NUMBERS
        else:
            if mode != Mode.OUTERSPACE:
                slices.append((start, i))
                start = i
                mode = Mode.OUTERSPACE

    if start < len(name) - 1:
        slices.append((start, len(name)))

    return [name[s[0] : s[1]].lower() for s in slices]


def camel_case(name: str) -> str:
    comps = name_to_components(name)
    if len(comps) == 0:
        return ""
    if len(comps) == 1:
        return comps[0].lower()
    else:
        return comps[0].lower() + "".join(
            comp.capitalize() for comp in comps[1:]
        )


def kebab_case(name: str) -> str:
    comps = name_to_components(name)
    return "-".join(comp.lower() for comp in comps)


def pascal_case(name: str) -> str:
    comps = name_to_components(name)
    return "".join(comp.capitalize() for comp in comps)


def scream_case(name: str) -> str:
    comps = name_to_components(name)
    return "_".join(comp.upper() for comp in comps)


def snake_case(name: str) -> str:
    comps = name_to_components(name)
    return "_".join(comp.lower() for comp in comps)
