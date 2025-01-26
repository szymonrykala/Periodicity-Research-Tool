from unittest.mock import MagicMock, patch

import pytest

from sprt.db.db import RandomTextDatabase
from sprt.text_generator import RandomText


@pytest.fixture
def mock_database():
    with patch("sprt.db.db_abc.Database._run") as mock_run:
        db = RandomTextDatabase(table_name="mock_table")
        yield db, mock_run


@pytest.fixture
def mock_random_text():
    mock_item = MagicMock(spec=RandomText)
    mock_item.id = "1234"
    mock_item.name = "test_name"
    mock_item.to_json.return_value = '{"id": "1234", "name": "test_name"}'
    return mock_item


def test_random_text_database_initialization(mock_database):
    db, mock_run = mock_database
    create_table_query = """
            CREATE TABLE IF NOT EXISTS {table}(
                id TEXT PRIMARY KEY,
                data "",
                created DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
    assert mock_run.call_count == 1
    mock_run.assert_called_with(create_table_query)


def test_random_text_database_get_all(mock_database):
    db, mock_run = mock_database
    mock_run.return_value = [("{'id': '1234', 'name': 'test_name'}",)]

    with patch("sprt.text_generator.RandomText.from_json") as mock_from_json:
        mock_item = MagicMock(spec=RandomText)
        mock_from_json.return_value = mock_item

        results = db.get_all()

        assert len(results) == 1
        assert results[0] == mock_item


def test_random_text_database_insert(mock_database, mock_random_text):
    db, mock_run = mock_database

    db.insert(mock_random_text)

    mock_run.assert_any_call(
        "INSERT INTO {table}(id, data) VALUES(:id, :data)",
        {"id": "1234", "data": '{"id": "1234", "name": "test_name"}'},
    )


def test_random_text_database_delete(mock_database, mock_random_text):
    db, mock_run = mock_database

    db.delete(mock_random_text)

    mock_run.assert_any_call("DELETE FROM {table} WHERE id=:id", {"id": "1234"})


def test_random_text_database_update(mock_database, mock_random_text):
    db, mock_run = mock_database

    db.update(mock_random_text)

    mock_run.assert_any_call(
        "UPDATE {table} SET data=:data WHERE id=:id",
        {"id": "1234", "data": '{"id": "1234", "name": "test_name"}'},
    )
