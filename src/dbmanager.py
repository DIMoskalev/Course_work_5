import psycopg2


class DBManager():

    def __init__(self, params: dict, dbname: str = 'hhru'):
        self.conn = psycopg2.connect(dbname=dbname, **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        with self.conn:
            self.cur.execute(
                """
                SELECT employer_name, COUNT(vacancy_id)
                FROM employers
                JOIN vacancies USING(employer_id)
                GROUP BY employer_name;
                """
            )
            return self.cur.fetchall()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты,
        а также ссылки на вакансию"""
        with self.conn:
            self.cur.execute(
                """
                SELECT employer_name, vacancy_name, salary_from, salary_to
                currency, vacancies.url
                FROM vacancies
                JOIN employers USING(employer_id);
                """
            )
            return self.cur.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        with self.conn:
            self.cur.execute(
                """
                SELECT(AVG(salary_from) + AVG(salary_to)) / 2 as tot_avg_salary
                FROM vacancies
                WHERE salary_from > 0 and salary_to > 0 and currency = 'руб.';
                """
            )
            return self.cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        with self.conn:
            self.cur.execute(
                """
                SELECT vacancy_name, employer_name, salary_from, salary_to, currency, vacancies.url
                FROM vacancies
                JOIN employers USING(employer_id)
                WHERE (salary_from + salary_to)/2 > (SELECT (AVG(salary_from) + AVG(salary_to)) / 2 as tot_avg_salary 
                FROM vacancies WHERE salary_from > 0 and salary_to > 0 and currency = 'руб.')
                and salary_from > 0 and salary_to > 0 and currency = 'руб.'; 
                """
            )
            return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        with self.conn:
            self.cur.execute(
                f"""
                SELECT vacancy_name, employer_name, salary_from, salary_to, currency, vacancies.url
                FROM vacancies
                JOIN employers USING(employer_id)
                WHERE employer_name LIKE '%{keyword}%' or requirement LIKE '%{keyword}%' 
                or responsibility LIKE '%{keyword}%';
                """
            )
            return self.cur.fetchall()
