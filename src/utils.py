from typing import Any
import requests
import psycopg2


def get_hh_data(employers_id: list[str]) -> list[dict[str, Any]]:
    """Получение данных о компаниях и вакансиях с помощью API hh.ru"""


def create_database(database_name: str, params: str) -> None:
    """Создание базы данных и таблиц для сохранения данных о компаниях и вакансиях"""


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """Сохранение данных о компаниях и вакансиях в базу данных"""
