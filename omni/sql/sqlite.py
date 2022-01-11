from pathlib import Path
from typing import Any
from typing import Union, Optional

from omni import check_soft_dependencies
from .base import CommitAndCloseBase

check_soft_dependencies("sqlite3")
import sqlite3  # noqa


def executemany_begin_wrap(cursor: sqlite3.Cursor, query: str, data: list[Any]) -> None:
    """Wrap execute many in begin commit to improve speed.

    If you are using `isolation_level=None` then you should use this!!! In such cases if execute many is not wrapped
    in BEGIN; {}; COMMIT; then it seems to run each line independently like a for loop. If we include the begin
    commit then it avoids this. See:
        https://stackoverflow.com/questions/35013453/apsw-or-sqlite3-very-slow-insert-on-executemany

    Arguments:
        cursor: The sqlite cursor object.
        query: The query to include.
        data: The list of values to execute.
    """
    cursor.execute("begin transaction")
    cursor.executemany(query, data)
    cursor.execute("commit")


class SQLite(CommitAndCloseBase):
    """Sqlite context manager class.

    Simple context manager wrapper around an sqlite file. Usage is as follows:
    ```
    with SQLite(sqlfile) as cursor:
        # Do things
    ```
    """

    def __init__(
        self, file: Union[Path, str], check_same_thread: bool = False, isolation_level: Optional[int] = None
    ) -> None:
        """
        Arguments:
            file: The location of the sqlite database to connect to.
            check_same_thread: A boolean that
        """
        self.file = file
        self.check_same_thread = check_same_thread
        self.isolation_level = isolation_level

    def __enter__(self) -> sqlite3.Cursor:
        self.connection = sqlite3.connect(
            self.file, check_same_thread=self.check_same_thread, isolation_level=self.isolation_level
        )
        self.connection.row_factory = sqlite3.Row
        return self.connection.cursor()
