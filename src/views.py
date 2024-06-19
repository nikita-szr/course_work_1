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


def get_cards_data(transactions):
    """Функция создает словарь с ключоми номеров карт и в значения добавляет сумму трат и сумму кэшбека"""
    card_data = {}
    for transaction in transactions:
        card_number = transaction.get('Номер карты')
        # если поле номер карты пустое операцию пропускаем т.к. не понятно к какой карте привязать трату
        if not card_number or str(card_number).strip().lower() == 'nan':
            continue
        amount = float(transaction['Сумма операции'])
        if card_number not in card_data:
            card_data[card_number] = {'total_spent': 0.0, 'cashback': 0.0}
        if amount < 0:
            card_data[card_number]['total_spent'] += amount
            cashback_value = transaction.get("Кэшбэк")
            # рассчитываем кэшбек как 1% от траты, но если поле кешбек содержит сумму просто ее добавляем
            if cashback_value is not None:
                cashback_amount = float(cashback_value)
                if cashback_amount >= 0:
                    card_data[card_number]['cashback'] += cashback_amount
                else:
                    card_data[card_number]['cashback'] += amount * -0.01
            else:
                card_data[card_number]['cashback'] += amount * 0.01
    cards_data = []
    for last_digits, data in card_data.items():
        cards_data.append({
            "last_digits": last_digits,
            "total_spent": round(data['total_spent'], 2),
            "cashback": round(data['cashback'], 2)})
    return cards_data
