"""Machine learning and pytorch helper functions."""
from itertools import islice

import os
from omni import check_soft_dependencies
from typing import Iterable, Any

check_soft_dependencies("numpy")
import numpy as np  # noqa


def get_freest_gpu() -> int:
    """Returns the gpu index that has the most available memory."""
    os.system("nvidia-smi -q -d Memory |grep -A4 GPU|grep Free >tmp")
    memory_available = [int(x.split()[2]) for x in open("tmp", "r").readlines()]
    return np.argmax(memory_available)


def batch_iterable(iterable: Iterable[Any], batch_size: int) -> Iterable[Iterable[Any]]:
    """Split into batches of the specified size."""
    iterator = iter(iterable)
    while batch := list(islice(iterator, batch_size)):
        yield batch
