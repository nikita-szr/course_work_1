import os

import pandas as pd
from dotenv import load_dotenv

from src.reports import spending_by_category, spending_by_weekday, spending_by_workday
from src.services import (analyze_cashback, find_person_to_person_transactions, investment_bank,
                          search_transaction_by_mobile_phone, search_transactions_by_user_choice)
from src.utils import get_data_from_xlsx
from src.views import main

# web сервисов
user_choice = {
    "user_currencies": ["USD", "EUR"],
    "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
}
load_dotenv()
api_key_currency = os.getenv("API_KEY_CURRENCY")
api_key_stocks = os.getenv("API_KEY_STOCKS")
input_date_str = "20.03.2020"
main_page = main(input_date_str, user_choice, api_key_currency, api_key_stocks)

# сервисы
transactions = get_data_from_xlsx(r'../data/operations.xls')
year = 2020
month = 5
date = "2020.05"
limit = 50
search = "Перевод"
cashback_analysis_result = analyze_cashback(transactions, year, month)
investment_bank_result = investment_bank(transactions, date, limit)
search_transactions_by_user_choice_result = search_transactions_by_user_choice(transactions, search)
search_transaction_by_mobile_phone_result = search_transaction_by_mobile_phone(transactions)
find_person_to_person_transactions_result = find_person_to_person_transactions(transactions)
print(cashback_analysis_result)
print(investment_bank_result)
print(search_transactions_by_user_choice_result)
print(search_transaction_by_mobile_phone_result)
print(find_person_to_person_transactions_result)


# отчёты
df = pd.read_excel(r'../data/operations.xls')
spending_by_category_result = spending_by_category(df, "Супермаркеты", "2020.05.20")
spending_by_weekday_result = spending_by_weekday(df, "2020.05.20")
spending_by_workday_result = spending_by_workday(df, "2020.05.20")
print(spending_by_category_result)
print(spending_by_weekday_result)
print(spending_by_workday_result)
