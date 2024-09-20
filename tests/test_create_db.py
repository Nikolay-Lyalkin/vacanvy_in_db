import psycopg2

from src.create_db import DB


def test_db_init(class_db):
    """Тест инициализации класса DB"""
    assert class_db.host == "localhost"
    assert class_db.database == "test_db"
    assert class_db.user == "postgres"
    assert class_db.password == "9998441653Qq"


def test_create_db(class_db):
    """Тест создания базы данных"""
    assert class_db.create_database() == "База данных создана!"


def test_create_table(class_db):
    """Тест создания таблиц"""
    assert class_db.create_table() == "Таблицы созданы"


def test_add_company_name(class_db):
    """Тест добавления названия компании"""
    assert class_db.add_company_name(["Газпром"]) == ["Газпром"]


def test_add_vacancy(class_db, class_hh):
    """Тест добавления вакансий"""
    assert class_db.add_vacancies(class_hh) == "Вакансии добавлены"
