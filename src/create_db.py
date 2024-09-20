import psycopg2

from src.get_vacancies_from_hh import HH


class DB:
    """Класс для создания базы данных"""

    def __init__(self, host: str, database: str, user: str, password: str):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.employers = []

    def create_database(self) -> str:
        """Метод создания базы данных"""
        conn = psycopg2.connect(dbname="postgres", user=self.user, password=self.password, host=self.host)
        cursor = conn.cursor()
        conn.autocommit = True
        sql = f"CREATE DATABASE {self.database}"
        cursor.execute(sql)
        cursor.close()
        conn.close()
        return "База данных создана!"

    def create_table(self) -> str:
        """Метод создания таблиц в базе данных"""
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("CREATE TABLE employers (employer_id serial PRIMARY KEY, company_name varchar UNIQUE)")
                    cur.execute(
                        "CREATE TABLE vacancies (vacancy_id serial PRIMARY KEY, vacancy_name varchar, \
                    employer_id int NOT NULL, salary_from int DEFAULT 0, city varchar, FOREIGN KEY (employer_id) \
                    REFERENCES employers(employer_id))"
                    )
        finally:
            conn.close()
        return "Таблицы созданы"

    def add_company_name(self, employers: list) -> list:
        """Метод заполнения таблицы компаний"""
        add_employers = []
        for employer in employers:
            if employer not in self.employers:
                self.employers.append(employer)
                add_employers.append(employer)
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        try:
            with conn:
                with conn.cursor() as cur:
                    for employer in add_employers:
                        cur.execute(f"INSERT INTO employers (company_name) VALUES (%s)", (employer,))
        finally:
            conn.close()
        return add_employers

    def add_vacancies(self, vacancies: HH) -> str:
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM employers")
                    rows = cur.fetchall()
                    for vacancy in vacancies.vacancies:
                        for row in rows:
                            if row[1] in vacancy["employer"] or row[1] in vacancy["vacancy_name"]:
                                cur.execute(
                                    "INSERT INTO vacancies (vacancy_name, employer_id, city, salary_from)\
                                 VALUES (%s, %s, %s, %s)",
                                    (vacancy["vacancy_name"], row[0], vacancy["city"], vacancy["salary"]),
                                )
        finally:
            conn.close()
        return "Вакансии добавлены"
