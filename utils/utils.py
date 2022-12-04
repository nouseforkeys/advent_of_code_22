"""
useful funcs for advent of code such as loading in the inputs
"""

from dataclasses import dataclass
import pathlib
from typing import Callable


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


@dataclass
class ParseConfig:
    """
    Class to contain a delimiter and how to parse each split item.
    """
    delimiter: str
    parser: 'Callable | ParseConfig | list[Callable | ParseConfig]'


def parse_from_file(file: pathlib.Path, parse_config: ParseConfig) -> list:
    """
    parses each line from a file recursively using the parse config.
    """
    lines = load_from_file(file)
    return [parse_string(line, parse_config) for line in lines]


def parse_string(string: str, parse_config: ParseConfig) -> list:
    """
    recursively parses a string using the parse_config to return a multi-level
    list object.

    The parse_config.parser argument:
    - The parse_config.delimiter will be used to split the string into segments
    - If the parser specified is Callable, this function will be called on each
    delimited string segment.
    - If the parser is a ParseConfig, this parse config will be applied to
    to each delimited string segment, creating sub-lists.
    - If the parser is a list the Callable or ParseConfig items in the list
    will be used to parse the corresponding delimited string segment by index.
    """
    segments = string.split(parse_config.delimiter)
    if isinstance(parse_config.parser, ParseConfig):
        return [
            parse_string(segment, parse_config.parser) for segment in segments]
    elif isinstance(parse_config.parser, list):
        if len(parse_config.parser) != len(segments):
            raise ValueError(
                'ParseConfig list not same length as delimited segments: '
                f'{parse_config}, {segments}')
        return [
            parser(segment) for parser, segment in
            zip(parse_config.parser, segments)]
    else:
        return [parse_config.parser(segment) for segment in segments]
