from src.create_db import DB
from src.database_manager import DBManager
from src.get_vacancies_from_hh import HH

host = ""
user = ""
name_db = ""
password = ""
hh_api = HH()
db_manager = DBManager(host, name_db, user, password)
database = DB(host, name_db, user, password)

create_db = database.create_database()  # Создание базы данных
create_table = database.create_table()  # Создание таблиц


def user_interaction():

    name_company = input("Введите названия компаний через запятую, вакансии которых вам интересны: ").split(",")
    get_vacancies = hh_api.get_vacancies(name_company)  # Получение вакансий с HH
    add_company = database.add_company_name(name_company)  # Заполнение таблицы работодателей
    add_vacancy = database.add_vacancies(hh_api)  # Заполнение таблицы вакансий

    output_result = int(
        input(
            """Какую информацию вы хотите получить?
                       1. Список всех компаний и количество вакансий у каждой
                       2. Получение всех вакансий
                       3. Среднюю зарплату по всем вакансиям
                       4. Список вакансий, у которых зарплата выше средней по всем вакансиям
                       5. Список вакансий, в названии которых будет присутствовать ключевое слово \n"""
        )
    )
    if output_result in range(1, 6):
        if output_result == 1:
            print(db_manager.get_companies_and_vacancies_count())
        elif output_result == 2:
            print(db_manager.get_all_vacancies())
        elif output_result == 3:
            print(db_manager.get_avg_salary())
        elif output_result == 4:
            print(db_manager.get_vacancies_with_higher_salary())
        elif output_result == 5:
            keyword = input("Введите слово для поиска по вакансиям")
            print(db_manager.get_vacancies_with_keyword(keyword))
    else:
        print("Вы ввели неверные данные")


if __name__ == "__main__":
    user_interaction()
