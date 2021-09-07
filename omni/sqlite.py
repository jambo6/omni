import sqlite3 as sqlite
from pathlib import Path
from typing import Any, Union, no_type_check


class CommitAndCloseBase:
    """Most will be finalised with commit and close, so we make into a base class."""

    connection: Any

    @no_type_check
    def __exit__(self, type_, value, traceback) -> None:
        self.connection.commit()
        self.connection.close()


class SQLite(CommitAndCloseBase):
    """Sqlite context manager class.

    Simple context manager wrapper around an sqlite file. Usage is as follows:
    ```
    with SQLite(sqlfile) as cursor:
        # Do things
    ```
    """

    def __init__(self, file: Union[Path, str], check_same_thread: bool = False) -> None:
        """
        Arguments:
            file: The location of the sqlite database to connect to.
            check_same_thread: A boolean that
        """
        self.file = file
        self.check_same_thread = check_same_thread

    def __enter__(self) -> sqlite.Cursor:
        self.connection = sqlite.connect(self.file, check_same_thread=self.check_same_thread)
        self.connection.row_factory = sqlite.Row
        return self.connection.cursor()
