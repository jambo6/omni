from pathlib import Path
from typing import Union

from base import CommitAndCloseBase

from omni import check_soft_dependencies

check_soft_dependencies("sqlite3")
import sqlite3  # noqa


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

    def __enter__(self) -> sqlite3.Cursor:
        self.connection = sqlite3.connect(self.file, check_same_thread=self.check_same_thread)
        self.connection.row_factory = sqlite3.Row
        return self.connection.cursor()
