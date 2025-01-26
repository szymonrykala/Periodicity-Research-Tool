from unittest.mock import MagicMock

import pytest

from sprt.db.db import RandomTextDatabase
from sprt.text_generator.distributions import Normal
from sprt.text_generator.generator import Generator
from sprt.text_generator.random_text import RandomText


@pytest.fixture
def generator_instance():
    return Generator()


@pytest.fixture
def normal_distribution():
    return Normal(mean=0.0, stdev=1.0)


@pytest.fixture
def db_instance():
    db = RandomTextDatabase("test_table")
    db._run = MagicMock()  # Mockujemy bezpośrednie zapytania do bazy
    return db


def test_generator_to_db_insertion(generator_instance, normal_distribution, db_instance):
    generated_text = generator_instance.generate(size=100, distrib=normal_distribution)
    assert isinstance(generated_text, RandomText)

    # Wstawienie do bazy danych
    db_instance.insert(generated_text)

    # Sprawdzenie, czy `insert` wywołał metodę `_run` z poprawnymi parametrami
    db_instance._run.assert_called_once_with(
        "INSERT INTO {table}(id, data) VALUES(:id, :data)",
        {"id": str(generated_text.id), "data": generated_text.to_json()},
    )


def test_db_retrieve_all(generator_instance, normal_distribution, db_instance):
    generated_text = generator_instance.generate(size=100, distrib=normal_distribution)
    assert isinstance(generated_text, RandomText)

    # Mock zwrócenia danych z bazy danych
    db_instance._run.return_value = [(generated_text.to_json(),)]

    # Pobranie wszystkich danych z bazy
    retrieved_texts = db_instance.get_all()
    assert len(retrieved_texts) == 1
    assert isinstance(retrieved_texts[0], RandomText)
    assert retrieved_texts[0].id == generated_text.id
    assert retrieved_texts[0].text.all() == generated_text.text.all()


def test_generator_to_db_and_back(generator_instance, normal_distribution, db_instance):
    generated_text = generator_instance.generate(size=100, distrib=normal_distribution)
    assert isinstance(generated_text, RandomText)

    # Wstawienie do bazy danych
    db_instance.insert(generated_text)

    # Mock zwrócenia danych z bazy danych
    db_instance._run.return_value = [(generated_text.to_json(),)]

    # Pobranie danych z bazy i porównanie
    retrieved_texts = db_instance.get_all()
    assert len(retrieved_texts) == 1
    retrieved_text = retrieved_texts[0]

    assert retrieved_text.id == generated_text.id
    assert retrieved_text.text.all() == generated_text.text.all()
    assert retrieved_text.distribution == generated_text.distribution
