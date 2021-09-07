from importlib import import_module


def check_soft_dependencies(*packages: str) -> None:
    """Check if soft dependencies are installed or raise an error.

    Arguments:
        packages: One or more package names

    Raises:
        ModuleNotFoundError: Error that notifies the required package is not installed.
    """
    for package in packages:
        try:
            import_module(package)
        except ModuleNotFoundError as e:
            raise ModuleNotFoundError(
                "{}\n{p} is a soft dependency that is not included in the base installation. If "
                "this module is required please manually install {p} via a pip install or otherwise.".format(
                    e, p=package
                )
            )
