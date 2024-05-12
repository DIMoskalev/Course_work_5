from typing import Any
import requests
import psycopg2


def get_hh_data(employers_id: list[str]) -> list[dict[str, Any]]:
    """Получение данных о компаниях и вакансиях с помощью API hh.ru"""
    data = []
    headers = {'User-Agent': 'HH-User-Agent'}
    params = {'text': '', 'page': 0, 'per_page': 100}
    for employer_id in employers_id:
        response_employer = requests.get('https://api.hh.ru/employers/' + employer_id,
                                         headers=headers, params=params)
        employer_data = response_employer.json()

        vacancy_data = []

        response_vacancy = requests.get('https://api.hh.ru/vacancies?employer_id=' + employer_id,
                                        headers=headers, params=params)
        response_vacancy_json = response_vacancy.json()
        vacancy_data.extend(response_vacancy_json['items'])

        data.append({
            'employers': employer_data,
            'vacancies': vacancy_data
        })
    return data


def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных и таблиц для сохранения данных о компаниях и вакансиях"""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute(f'DROP DATABASE {database_name}')
    except psycopg2.errors.InvalidCatalogName:
        pass
    cur.execute(f'CREATE DATABASE {database_name}')

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname='postgres', **params)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employers(
                employer_id SERIAL PRIMARY KEY,
                employer_name VARCHAR NOT NULL,
                description TEXT,
                area VARCHAR,
                url VARCHAR NOT NULL
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies(
                vacancy_id SERIAL PRIMARY KEY,
                vacancy_name VARCHAR NOT NULL,
                employer_id INT REFERENCES employers(employer_id) NOT NULL,
                employment VARCHAR,
                experience VARCHAR,
                professional_roles VARCHAR,
                salary INT,
                url VARCHAR NOT NULL
            )
        """)

    conn.commit()
    conn.close()


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """Сохранение данных о компаниях и вакансиях в базу данных"""
