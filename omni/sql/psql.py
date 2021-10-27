from typing import Optional

from omni import check_soft_dependencies

from .base import CommitAndCloseBase

check_soft_dependencies("psycopg2")
import psycopg2  # noqa


class PSQL(CommitAndCloseBase):
    """Postgres context manager class."""

    def __init__(self, database: str, user: str, password: Optional[str] = None) -> None:
        """
        Arguments:
            database: The name of the database to connect to.
        """
        self.database = database
        self.user = user
        self.password = password

    def __enter__(self) -> psycopg2:
        self.connection = psycopg2.connect(database=self.database, user=self.user, password=self.password)
        return self.connection.cursor()
