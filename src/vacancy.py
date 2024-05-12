class Vacancy:
    """Класс для работы с вакансиями"""

    def __init__(self, name, professional_roles, experience, employment, schedule,
                 salary_from, salary_to, currency, requirement, responsibility, url):
        self.name = name
        self.professional_roles = professional_roles
        self.experience = experience
        self.employment = employment
        self.schedule = schedule
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.requirement = requirement
        self.responsibility = responsibility
        self.url = url

    @classmethod
    def data_conversion(cls, vacancies_data):
        """Класс-метод для создания экземпляров класса"""
        emp_list = []
        for vacancy in vacancies_data:
            name = cls.check_data_str(vacancy['name'])
            professional_roles = cls.check_data_str(vacancy['professional_roles'][0]['name'])
            experience = cls.check_data_str(vacancy.get('experience').get('name'))
            employment = cls.check_data_str(vacancy['employment']['name'])
            schedule = cls.check_data_str(vacancy['schedule']['name'])
            if not vacancy['salary']:
                salary_from = 0
                salary_to = 0
                currency = 0
            else:
                salary_from = cls.check_data_int(vacancy['salary']['from'])
                salary_to = cls.check_data_int(vacancy['salary']['to'])
                currency = cls.decode_currency(cls.check_data_str(vacancy['salary']['currency']))
            requirement = cls.check_data_str(vacancy['snippet']['requirement'])
            responsibility = cls.check_data_str(vacancy['snippet']['responsibility'])
            url = vacancy['alternate_url']
            object_vac = cls(name, professional_roles, experience, employment, schedule,
                             employer, salary_from, salary_to, currency, requirement,
                             responsibility, url)
            emp_list.append(object_vac)
        return emp_list

    @classmethod
    def get_objects_for_data_conversion(cls, vacancies_list):
        """Класс-метод для создания ЭК из словарей формата Vacancy.__dict__,
        получаемых при выгрузке вакансий из файла"""
        returned_list = []
        for vacancy in vacancies_list:
            name = vacancy['name']
            professional_roles = vacancy['professional_roles']
            experience = vacancy['experience']
            employment = vacancy['employment']
            schedule = vacancy['schedule']
            salary_from = vacancy['salary_from']
            salary_to = vacancy['salary_to']
            currency = vacancy['currency']
            requirement = vacancy['requirement']
            responsibility = vacancy['responsibility']
            url = vacancy['url']
            vacancy_object = cls(name, professional_roles, experience, employment, schedule,
                                 salary_from, salary_to, currency, requirement,
                                 responsibility, url)
            returned_list.append(vacancy_object)
        return returned_list

    def data_for_db(self):
        return [self.name, self.professional_roles, self.experience, self.employment, self.schedule,
                self.salary_from, self.salary_to, self.currency, self.requirement, self.responsibility,
                self.url]

    def get_salary(self):
        """Метод, направленный на обработку истинности диапазона заработной платы"""
        if not (self.salary_to or self.salary_from):
            return f'Зарплата: Не указана'
        else:
            if not self.salary_to:
                return f'Зарплата: от {self.salary_from} {self.currency}'
            elif not self.salary_from:
                return f'Зарплата: до {self.salary_to} {self.currency}'
            elif self.salary_from == self.salary_to:
                return f'Зарплата: {self.salary_to} {self.currency}'
            return f'Зарплата: от {self.salary_from} до {self.salary_to} {self.currency}'

    @staticmethod
    def decode_currency(currency):
        """Метод, направленный на расшифровку валюты из кодового обозначения"""
        currency_dict = {
            "RUR": "руб.",
            "KZT": "тенге",
            "BYR": "белорус. руб",
            "UZS": "узбек. сум",
            "USD": "долл.",
            "EUR": "евро",
            "": "попугаев"
        }
        if currency:
            return currency_dict.get(currency, f'Неизвестная валюта {currency}')
        else:
            return ""

    @staticmethod
    def check_data_str(data):
        """Статик-метод для проверки существования строковых значений(str)"""
        if data:
            return data
        else:
            return 'Данные не указаны'

    @staticmethod
    def check_data_int(data):
        """Статик-метод для проверки существования целочисленных значений(int)"""
        if data:
            return data
        return 0

    def __gt__(self, other):  # Для сравнения если >
        if not isinstance(other, (Vacancy, int)):
            raise TypeError("Значение справа должно иметь тип int или принадлежать классу Vacancy")
        if type(other) is type(self):
            return self.salary_from > other.salary_from
        return self.salary_from > other

    def __ge__(self, other):  # Для сравнения если >=
        if not isinstance(other, (Vacancy, int)):
            raise TypeError("Значение справа должно иметь тип int или принадлежать классу Vacancy")
        if type(other) is type(self):
            return self.salary_from >= other.salary_from
        return self.salary_from >= other

    def __le__(self, other):  # Для сравнения если <=
        if not isinstance(other, (Vacancy, int)):
            raise TypeError("Значение справа должно иметь тип int или принадлежать классу Vacancy")
        if type(other) is type(self):
            return self.salary_from <= other.salary_from
        return self.salary_from <= other

    def __str__(self):
        return (f'-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-'
                f'\nВакансия: {self.name}\n'
                f'Должность: {self.professional_roles}\n'
                f'Требуемый опыт: {self.experience}\n'
                f'Тип занятости: {self.employment}\n'
                f'График: {self.schedule}\n'
                f'{self.get_salary()}\n'
                f'Работодатель: {self.employer}\n'
                f'Требования: {self.requirement.replace("<highlighttext>", "").replace("</highlighttext>", "")}\n'
                f'Обязанности: {self.responsibility.replace("<highlighttext>", "").replace("</highlighttext>", "")}\n'
                f'Ссылка на вакансию: {self.url}\n'
                f'-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-')
