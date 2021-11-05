import joblib
import multiprocessing
from typing import Any, Callable


class UnavailableResourceError(Exception):
    pass


def parallel_for_loop(
    func: Callable[[Any], Any], args: list[tuple[Any, ...]], num_cpus: int = -1, backend: str = "joblib"
) -> list[Any]:
    """Function for running for loops in parallel.

    Args:
        func: The function to call in parallel.
        args: A list of tuples where each tuple will be mapped into the args of func.
        num_cpus: The number of cpus to utilise, defaults to -1 which corresponds to all.
        backend: The method to use ('joblib', 'multiprocessing').

    Returns:
        A list of the function outputs.
    """
    # Some checks
    total_cpus = multiprocessing.cpu_count()
    if num_cpus == -1:
        num_cpus = total_cpus
    if num_cpus > total_cpus:
        raise UnavailableResourceError("You have {} cpus but requested {}".format(total_cpus, num_cpus))

    assert num_cpus <= multiprocessing.cpu_count()

    def unpack_func(args: list[tuple[Any, ...]]):
        return func(*args)

    # In parallel
    if num_cpus > 1:
        if backend == 'joblib':
            results = joblib.Parallel(n_jobs=num_cpus)(
                joblib.delayed(unpack_func)(arg) for arg in args
            )
        elif backend == 'threading':
            results = joblib.Parallel(n_jobs=num_cpus, backend='threading')(
                joblib.delayed(unpack_func)(arg) for arg in args
            )
        elif backend == 'multiprocessing':
            with multiprocessing.Pool(num_cpus) as pool:
                results = pool.starmap(func, args)
        else:
            raise NotImplementedError()
    # Otherwise run a normal loop
    else:
        results = []
        for arg in args:
            results.append(func(*arg))

    return results
