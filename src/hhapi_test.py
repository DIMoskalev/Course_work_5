import requests


class HeadhunterAPI:
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self):
        self.url = ''
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.vacancies = []
        self.employers = []

    def load_vacancies(self, employers_id, keyword: str = ''):
        """Метод осуществляет поиск вакансий на сайте HH.ru по ключевому слову keyword,
        и возвращает список вакансий, которые были получены с HH.ru"""
        for employer_id in employers_id:
            self.url = 'https://api.hh.ru/vacancies?employer_id=' + employer_id
            self.params['text'] = keyword
            while self.params.get('page') != 20:
                response = requests.get(self.url, headers=self.headers, params=self.params)
                vacancies = response.json()['items']
                self.vacancies.extend(vacancies)
                self.params['page'] += 1
            return self.vacancies

    def load_employers(self, employers_id: list):
        """Метод получает список id работодателей(компаний) и возвращает список с информацией о работодателях
        (компаниях)"""
        for employer_id in employers_id:
            self.url = 'https://api.hh.ru/employers/' + employer_id
            response = requests.get(self.url, headers=self.headers, params=self.params)
            self.employers.append(response.json())
        return self.employers
