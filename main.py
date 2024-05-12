from config import config
from src.dbmanager import DBManager
from src.utils import get_hh_data, save_data_to_database, create_database


def main():
    employers_id = [
        '3127',  # ПАО Мегафон
        '2748',  # ПАО Ростелеком
        '665467',  # ГринАтом
        '84585',  # Avito
        '1942330',  # Пятерочка
        '3707941',  # Цитадель
        '1057',  # Лаборатория Касперского
        '1740',  # Яндекс
        '87021',  # WILDBERRIES
        '15478',  # VK
    ]
    params = config()

    data = get_hh_data(employers_id)
    create_database('hhru', params)
    save_data_to_database(data, 'hhru', params)

    # db = DBManager(params)

# Здесь будет основной код работы консольной программы


if __name__ == "__main__":
    main()
