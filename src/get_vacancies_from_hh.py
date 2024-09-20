from typing import Any

import requests


class HH:
    """
    Класс для работы с API HeadHunter

    """

    def __init__(self) -> None:
        self.url = "https://api.hh.ru/vacancies"
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params = {"text": "", "page": 0, "per_page": 100}
        self.vacancies = []

    def get_vacancies(self, keywords: list) -> Any:
        """Метод для получения вакансий с платформы HH, принимает на слово по которому осуществляется поиск"""
        for keyword in keywords:
            self.params["page"] = 0
            self.params["text"] = keyword
            while self.params.get("page") != 20:
                response = requests.get(self.url, headers=self.headers, params=self.params)
                result = response.status_code
                vacancies = response.json()["items"]
                for vacancy in vacancies:
                    if vacancy["salary"]:
                        self.vacancies.append(
                            {
                                "vacancy_name": vacancy["name"],
                                "employer": vacancy["employer"]["name"],
                                "salary": vacancy["salary"]["from"],
                                "city": vacancy["area"]["name"],
                            }
                        )
                    else:
                        self.vacancies.append(
                            {
                                "vacancy_name": vacancy["name"],
                                "employer": vacancy["employer"]["name"],
                                "salary": 0,
                                "city": vacancy["area"]["name"],
                            }
                        )

                self.params["page"] += 1
        return self.vacancies
