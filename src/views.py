import pandas as pd
from typing import Dict, List
from datetime import datetime


def get_data_from_xlsx(path: str) -> List[Dict]:
    """Функция принимает путь до xlsx файла и создает список словарей с транзакциями"""
    try:
        df = pd.read_excel(path)
        return df.to_dict(orient='records')
    except Exception as e:
        print(f'Возникла ошибка {e}')
        return []


def filter_transactions_by_date(transactions):
    """Функция принимает список словарей с транзакциями и фильтрует по дате
    от начала текущего месяца по сегодняшний день"""
    end_date = datetime.now()
    start_date = datetime(end_date.year, end_date.month, 1)

    def parse_date(date_str):
        """Функция переводит дату из формата строки в формат datetime"""
        return datetime.strptime(date_str, '%d.%m.%Y %H:%M:%S')

    filtered_transactions = [transaction for transaction in transactions
                             if start_date <= parse_date(transaction["Дата операции"]) <= end_date]
    return filtered_transactions


def greeting():
    """Функция определяет время суток и возвращает приветствие в зависимости от времени"""
    now = datetime.now()
    current_hour = now.hour
    if 6 <= current_hour < 12:
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    elif 18 <= current_hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"

