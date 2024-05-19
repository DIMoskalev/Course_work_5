from src.utils import work_with_data_from_db, work_with_vacancies_from_api, work_with_vacancies_from_json


def main():
    print("Добро пожаловать в программу по поиску и работе с вакансиями!")
    while True:
        start_input = input('Пока что не весь доп. функционал добавлен, обновления будут в ближайшее время.\n'
                            'Чтобы начать работу программы нажмите Enter и следуйте инструкциям.\n'
                            'В любой момент вы можете ввести "стоп" или "stop" и программа завершит работу.\n')
        while start_input not in ['stop', 'стоп']:
            user_input = input('Выберите, в каком виде вы хотите работать с вакансиями.\n'
                               '1 - Программа предоставит возможность работать с вакансиями в БД PostgreSQL\n'
                               '2 - Программа предоставит возможность работать с вакансиями с сайта hh.ru\n'
                               '3 - Программа предоставит возможность работать с вакансиями из json-файла\n').lower()
            if user_input == '1':
                work_with_data_from_db()
            if user_input == '2':
                work_with_vacancies_from_api()
            elif user_input == '3':
                work_with_vacancies_from_json()
            elif user_input in ['stop', 'стоп']:
                quit()
            else:
                print('Нужно выбрать режим работы из представленных ранее (либо 1, либо 2)\n')
        break


if __name__ == "__main__":
    main()
