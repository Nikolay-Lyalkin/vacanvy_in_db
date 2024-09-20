import psycopg2
import pytest

from src.create_db import DB
from src.database_manager import DBManager
from src.get_vacancies_from_hh import HH


@pytest.fixture
def class_db():
    return DB("localhost", "test_db", "postgres", "9998441653Qq")


@pytest.fixture
def class_hh():
    hh_vacancy = HH()
    hh_vacancy.vacancies.append(
        {
            "vacancy_name": "Менеджер",
            "employer": "Газпром",
            "salary": 100000,
            "city": "Москва",
        }
    )
    hh_vacancy.vacancies.append(
        {
            "vacancy_name": "Управляющий",
            "employer": "Газпром",
            "salary": 130000,
            "city": "Москва",
        }
    )
    return hh_vacancy


@pytest.fixture
def class_db_manager():
    return DBManager("localhost", "test_db", "postgres", "9998441653Qq")
