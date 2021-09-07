from typing import Any, no_type_check


class CommitAndCloseBase:
    """Most will be finalised with commit and close, so we make into a base class."""

    connection: Any

    @no_type_check
    def __exit__(self, type_, value, traceback) -> None:
        self.connection.commit()
        self.connection.close()
