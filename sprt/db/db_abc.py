from abc import ABC, abstractmethod
from sqlite3 import Connection, Cursor

from sprt.config import DB_FILE


class Query(ABC):
    @abstractmethod
    def _execute(self, cursor: Cursor):
        pass


class Database(ABC):
    def __init__(self, table_name: str):
        self._table = table_name
        self.__db = Connection(database=DB_FILE, check_same_thread=False, isolation_level=None)

    @property
    def table(self):
        return self._table

    def _run(self, sql_query: str, params=[]) -> list[tuple[str, str]]:
        with self.__db:
            cursor = self.__db.cursor()
            result = cursor.execute(sql_query.format(table=self.table), params).fetchall()

        return result
