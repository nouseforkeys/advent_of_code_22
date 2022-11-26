"""
useful funcs for advent of code such as loading in the inputs
"""

import pathlib


def load_from_file(
    file: pathlib.Path,
    cast_as: type | list[type] = str, delimiter: str = ','
) -> list:
    """
    returns the contents of a file as a list where each item in the list was
    delimited in the file by the character passed.

    Each line is then cast as a the types specified.
    """
    with open(file, 'r') as f:
        line_list = [line.strip() for line in f.readlines()]

    parsed_lines = []
    if isinstance(cast_as, list):
        for line in line_list:
            parsed_lines.append(
                [cast(item) for cast, item in
                    zip(cast_as, line.split(delimiter))]
            )
    else:
        for line in line_list:
            parsed_lines.append(cast_as(line))

    return parsed_lines
