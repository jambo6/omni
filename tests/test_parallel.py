import time
from omni import parallel


def _delayed_function(x: int, y: int) -> tuple[int, int]:
    """Random delayed function."""
    print(x, y)
    time.sleep(3)
    return x + 1, y + 1


def test_parallel_for_loop():
    # Check parallel works
    args = [(1, 2), (2, 3), (3, 4)]
    outputs = parallel.parallel_for_loop(_delayed_function, args, num_cpus=5)
    assert outputs == [(x + 1, y + 1) for x, y in args]
    mp_outputs = parallel.parallel_for_loop(_delayed_function, args, num_cpus=5, backend='multiprocessing')
    assert mp_outputs == outputs

    # Check parallel gives the same as normal
    print('completed!')
    time.sleep(1)
    assert outputs == parallel.parallel_for_loop(_delayed_function, args, num_cpus=1)
