import pandas as pd
from typing import Dict, List
from datetime import datetime
import requests
from dotenv import load_dotenv


def get_data_from_xlsx(path: str) -> List[Dict]:
    """Функция принимает путь до xlsx файла и создает список словарей с транзакциями"""
    try:
        df = pd.read_excel(path)
        return df.to_dict(orient='records')
    except Exception as e:
        print(f'Возникла ошибка {e}')
        return []


def filter_transactions_by_date(transactions, input_date_str): # дата формата дд.мм.гггг.
    """Функция принимает список словарей с транзакциями и дату
    фильтрует транзакции с начала месяца, на который выпадает входящая дата по входящую дату."""
    input_date = datetime.strptime(input_date_str, '%d.%m.%Y')
    end_date = input_date
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
            card_data[card_number]['total_spent'] += abs(amount)
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


def get_top_5_transactions(transactions):
    """Функция принимает список транзакций и выводит топ 5 операций по сумме платежа"""
    sorted_transactions = sorted(transactions, key=lambda x: float(x["Сумма операции"]), reverse=True)
    top_5_sorted_transactions = []
    for transaction in sorted_transactions[:5]:
        date = datetime.strptime(transaction["Дата операции"], '%d.%m.%Y %H:%M:%S').strftime('%d.%m.%Y')
        top_5_sorted_transactions.append({
            "date": date,
            "amount": transaction["Сумма операции"],
            "category": transaction["Категория"],
            "description": transaction["Описание"]
        })
    return top_5_sorted_transactions


def get_exchange_rates(currencies, api_key_currency):  # не забыть что функция принимает список ["USD", "EUR"]
    """Функция принимает список кодов валют и возвращает список словарей с валютами и их курсами"""
    exchange_rates = []
    for currency in currencies:
        url = f'https://v6.exchangerate-api.com/v6/{api_key_currency}/latest/{currency}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            ruble_cost = data["conversion_rates"]["RUB"]
            exchange_rates.append({
                "currency": currency,
                "rate": ruble_cost})
        else:
            print(f"Ошибка: {response.status_code}, {response.text}")
            exchange_rates.append({
                "currency": currency,
                "rate": None
            })
    return exchange_rates


def get_stocks_cost(companies, api_key_stocks):  # не забыть что функция принимает список ["AAPL", "AMZN", "GOOGL"]
    """Функция принимает список кодов компаний и возвращает словарь со стоимостью акций каждой переданной компании"""
    stocks_cost = []
    for company in companies:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={company}&apikey={api_key_stocks}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            time_series = data.get("Time Series (Daily)")
            if time_series:
                latest_date = max(time_series.keys())
                latest_data = time_series[latest_date]
                stock_cost = latest_data["4. close"]
                stocks_cost.append({
                    "stock": company,
                    "price": float(stock_cost)})
            else:
                print(f"Ошибка: данные для компании {company} недоступны.")
                stocks_cost.append({
                    "stock": company,
                    "price": None})
        else:
            print(f"Ошибка: {response.status_code}, {response.text}")
            stocks_cost.append({
                "stock": company,
                "price": None})
    return stocks_cost
