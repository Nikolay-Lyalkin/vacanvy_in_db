import psycopg2


class DBManager:
    def __init__(self, host: str, database: str, user: str, password: str):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def get_companies_and_vacancies_count(self) -> str:
        """Метод возвращает список всех компаний и количество вакансий у каждой компании."""
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        result = ""
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT employers.company_name, COUNT(*) \
                    FROM vacancies \
                    JOIN employers ON vacancies.employer_id = employers.employer_id \
                    GROUP BY employers.company_name"
                    )
                    rows = cur.fetchall()
                    for row in rows:
                        result += f"{row[0]}: {row[1]} вакансий\n"
        finally:
            conn.close()
        return result

    def get_all_vacancies(self) -> str:
        """Метод для получения всех вакансий"""
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        result = ""
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT employers.company_name, vacancies.vacancy_name, vacancies.salary_from, vacancies.city \
                    FROM vacancies \
                    JOIN employers ON vacancies.employer_id = employers.employer_id"
                    )
                    rows = cur.fetchall()
                    for row in rows:
                        result += f'"компания": {row[0]}, "вакансия": {row[1]}, "зарплата": {row[2]}, \
"город": {row[3]}\n'
        finally:
            conn.close()
        return result

    def get_avg_salary(self) -> str:
        """Метод возвращает среднюю зарплату по вакансиям"""
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT ROUND(AVG(salary_from), 2) as average_salary \
                    FROM vacancies \
                    WHERE salary_from IS NOT NULL AND salary_from > 0"
                    )
                    rows = cur.fetchall()
                    return f"Средняя зарплата: {rows[0][0]}"
        finally:
            conn.close()

    def get_vacancies_with_higher_salary(self) -> str:
        """Возвращает список вакансий, у которых зарплата выше средней по всем вакансиям"""
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        result = ""
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT employers.company_name, vacancies.vacancy_name, vacancies.salary_from, \
                    vacancies.city \
                    FROM vacancies \
                    JOIN employers ON vacancies.employer_id = employers.employer_id \
                    WHERE vacancies.salary_from > (SELECT AVG(salary_from) \
                    FROM vacancies \
                    WHERE salary_from IS NOT NULL AND salary_from > 0)"
                    )
                    rows = cur.fetchall()
                    for row in rows:
                        result += f'"компания": {row[0]}, "вакансия": {row[1]}, "зарплата": {row[2]}, \
"город": {row[3]}\n'
        finally:
            conn.close()
        return result

    def get_vacancies_with_keyword(self, *args) -> str:
        """Возвращает список вакансий, в названии которых содержатся переданные в метод слова"""
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        result = ""
        try:
            with conn:
                with conn.cursor() as cur:
                    for arg in args:
                        cur.execute(
                            f"SELECT employers.company_name, vacancies.vacancy_name, vacancies.salary_from, \
                                vacancies.city \
                                FROM vacancies \
                                JOIN employers ON vacancies.employer_id = employers.employer_id \
                                WHERE vacancy_name LIKE '%{arg}%'"
                        )
                        rows = cur.fetchall()
                        for row in rows:
                            result += f'"компания": {row[0]}, "вакансия": {row[1]}, "зарплата": {row[2]}, \
"город": {row[3]}\n'

        finally:
            conn.close()
        return result
