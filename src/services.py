
import json
from typing import List, Dict
from datetime import datetime


def analyze_cashback(data: List[Dict], year: int, month: int) -> json:
    """Принимает список словарей транзакций и считает сумму кэшбека по категориям"""
    cashback_analysis = {}
    for transaction in data:
        transaction_date = datetime.strptime(transaction["Дата операции"], '%d.%m.%Y %H:%M:%S')
        if transaction_date.year == year and transaction_date.month == month:
            category = transaction["Категория"]
            amount = transaction["Сумма операции"]
            if amount < 0:
                cashback_value = transaction["Кэшбэк"]
                if cashback_value >= 0:
                    cashback = cashback_value
                else:
                    cashback = round(amount * -0.01, 5)
                if category in cashback_analysis:
                    cashback_analysis[category] += cashback
                else:
                    cashback_analysis[category] = cashback
    return json.dumps(cashback_analysis, ensure_ascii=False, indent=4)

