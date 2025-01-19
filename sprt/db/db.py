from concurrent.futures import ThreadPoolExecutor
from typing import Callable

from sprt.logger import logger
from sprt.text_generator import RandomText

from .db_abc import Database


class RandomTextDatabase(Database):
    def __init__(self, table_name: str):
        super().__init__(table_name)
        self._create_text_store()

    def _create_text_store(self):
        self._run(
            """
            CREATE TABLE IF NOT EXISTS {table}(
                id TEXT PRIMARY KEY,
                data "",
                created DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

    def get_all(self):
        resp = self._run("SELECT data FROM {table}")
        logger.info(f"'{len(resp)}' item read from database")

        return [RandomText.from_json(item[0]) for item in resp]

    def get_all_async(self, append_callback: Callable[[RandomText], None]):
        resp = self._run("SELECT data FROM {table}")
        logger.info(f"'{len(resp)}' item read from database")

        def _job(data: str):
            item = RandomText.from_json(data)

            append_callback(item=item)

        logger.info(f"Async loading items from database")
        with ThreadPoolExecutor(3) as exec:
            exec.map(_job, map(lambda v: v[0], resp))

    def insert(self, item: RandomText) -> None:
        logger.debug(f"saving to database '{item.name}' '{item.id}' text set")
        self._run(
            "INSERT INTO {table}(id, data) VALUES(:id, :data)",
            {"id": str(item.id), "data": item.to_json()},
        )

    def delete(self, item: RandomText) -> None:
        logger.debug(f"deleting '{item.id}' text set from database")
        self._run("DELETE FROM {table} WHERE id=:id", {"id": str(item.id)})

    def update(self, item: RandomText) -> None:
        logger.debug(f"Updating '{item.id}' text set to database")
        self._run(
            "UPDATE {table} SET data=:data WHERE id=:id",
            {"id": str(item.id), "data": item.to_json()},
        )
