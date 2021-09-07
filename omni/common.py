import os
import time
from pathlib import Path
from typing import Any, Union, no_type_check


def read_text_file(filename: str) -> str:
    """Read a text file into a string"""
    with open(filename) as file:
        output = file.read()
    return output


def make_directory_if_not_exists(directory: Union[Path, str]) -> None:
    """Makes a directory if one does not already exist at the specified location."""
    if not os.path.isdir(directory):
        os.mkdir(directory)


def unpack_list_of_lists(list_of_lists: list[list[Any]]) -> list[Any]:
    """Unpacks a list of lists into a single list."""
    return [x for y in list_of_lists for x in y]


@no_type_check
def timeit(method):
    """Decorator for timing functions."""

    def timed(*args, **kwargs):
        # Run and time method
        start_time = time.time()
        result = method(*args, **kwargs)
        end_time = time.time()

        # Print timing information
        print("{}: {:.2f}s".format(method.__name__, (end_time - start_time)))

        return result

    return timed
