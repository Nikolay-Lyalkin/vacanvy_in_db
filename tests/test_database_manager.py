def test_db_manager_init(class_db_manager):
    """Тест инициализации класса DBManager"""
    assert class_db_manager.host == "localhost"
    assert class_db_manager.database == "test_db"
    assert class_db_manager.user == "postgres"
    assert class_db_manager.password == "9998441653Qq"


def test_get_companies_and_vacancies_count(class_db_manager):
    """Тест получения названия компаний и количества вакансий каждой"""
    assert class_db_manager.get_companies_and_vacancies_count().strip() == "Газпром: 2 вакансий"


def test_get_all_vacancies(class_db_manager):
    """Тест получений всех вакансий"""
    assert (
        class_db_manager.get_all_vacancies()
        == '"компания": Газпром, "вакансия": Менеджер, \
"зарплата": 100000, "город": Москва\n"компания": Газпром, "вакансия": Управляющий, \
"зарплата": 130000, "город": Москва\n'
    )


def test_get_avg_salary(class_db_manager):
    """Тест получения средней зарплаты по всем вакансиям, где она указана"""
    assert class_db_manager.get_avg_salary() == "Средняя зарплата: 115000.00"


def test_get_vacancies_with_higher_salary(class_db_manager):
    """Тест получения вакансий, где зарплата вышей средней по всем вакансиям"""
    assert (
        class_db_manager.get_vacancies_with_higher_salary().strip()
        == '"компания": Газпром, "вакансия": Управляющий, \
"зарплата": 130000, "город": Москва'
    )


def test_get_vacancies_with_keyword(class_db_manager):
    """Тест получения вакансий в которых присутствует ключевое слово"""
    assert (
        class_db_manager.get_vacancies_with_keyword("Менеджер").strip()
        == '"компания": Газпром, "вакансия": Менеджер, \
"зарплата": 100000, "город": Москва'
    )
