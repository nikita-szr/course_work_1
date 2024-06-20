import json
import re
from datetime import datetime
from typing import Dict, List


def analyze_cashback(transactions: List[Dict], year: int, month: int) -> str:
    """Принимает список словарей транзакций и считает сумму кэшбека по категориям"""
    cashback_analysis: Dict = {}
    for transaction in transactions:
        transaction_date = datetime.strptime(transaction["Дата операции"], '%d.%m.%Y %H:%M:%S')
        if transaction_date.year == year and transaction_date.month == month:
            category = transaction["Категория"]
            amount = transaction["Сумма операции"]
            if amount < 0:
                cashback_value = transaction["Кэшбэк"]
                if cashback_value is not None and cashback_value >= 0:
                    cashback = float(cashback_value)
                else:
                    cashback = round(amount * -0.01, 5)
                if category in cashback_analysis:
                    cashback_analysis[category] += cashback
                else:
                    cashback_analysis[category] = cashback
    return json.dumps(cashback_analysis, ensure_ascii=False, indent=4)


def investment_bank(transactions: List[Dict], date: str, limit: int) -> int:  # принимает строку с датой гггг.мм
    """Функция принимает транзакции, дату и лимит округления и считает сколько можно было отложить в инвесткопилку"""
    sum_investment_bank = 0
    user_date = datetime.strptime(date, '%Y.%m')
    for transaction in transactions:
        transaction_date = datetime.strptime(transaction["Дата операции"], '%d.%m.%Y %H:%M:%S')
        if transaction_date.year == user_date.year and transaction_date.month == user_date.month:
            amount = transaction["Сумма операции"]
            if amount < 0 and transaction["Категория"] != "Переводы" and transaction["Категория"] != "Наличные":
                amount_ = abs(amount)  # перевел в положительное
                total_amount = ((amount_ + limit + 1) // limit) * limit - amount_
                sum_investment_bank += total_amount
    return sum_investment_bank


def search_transactions_by_user_choice(transactions: List[Dict], search: str) -> str:
    """Функция выполняет поиск в транзакциях по переданной строке """
    search_result = []
    for transaction in transactions:
        category = str(transaction.get('Категория', ''))
        description = str(transaction.get('Описание', ''))
        if search.lower() in description.lower() or search.lower() in category.lower():
            search_result.append(transaction)
    return json.dumps(search_result, ensure_ascii=False, indent=4)


def search_transaction_by_mobile_phone(transactions: List[Dict]) -> str:
    """Функция возвращает транзакции в описании которых есть мобильный номер"""
    mobile_pattern = re.compile(r'\+\d{1,4}')
    found_transactions = []
    for transaction in transactions:
        description = transaction.get('Описание', '')
        if mobile_pattern.search(description):
            found_transactions.append(transaction)
    return json.dumps(found_transactions, ensure_ascii=False, indent=4)


def find_person_to_person_transactions(transactions: List[Dict]) -> str:
    """Функция вовзращает транзакции в описании которых есть имя кому или от кого выполнен перевод"""
    transfer_transactions = []
    search_pattern = re.compile(r'\b[А-ЯЁ][а-яё]*\s[А-ЯЁ]\.')
    for transaction in transactions:
        category = transaction.get('Категория', '')
        description = transaction.get('Описание', '')
        if category == 'Переводы' and search_pattern.search(description):
            transfer_transactions.append(transaction)
    return json.dumps(transfer_transactions, ensure_ascii=False, indent=4)
