import os
import json
from src.views import get_data_from_xlsx, filter_transactions_by_date, greeting, get_cards_data, get_top_5_transactions, \
    get_exchange_rates, get_stocks_cost
from dotenv import load_dotenv

user_choice = {
    "user_currencies": ["USD", "EUR"],
    "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
}
load_dotenv()
api_key_currency = os.getenv("API_KEY_CURRENCY")
api_key_stocks = os.getenv("API_KEY_STOCKS")
input_date_str = "20.05.2020"


def main(input_date, user_settings, api_key_currency, api_key_stocks):
    """Основная функция для генерации JSON-ответа."""
    transactions = get_data_from_xlsx(r'../data/operations.xls')
    filtered_transactions = filter_transactions_by_date(transactions, input_date)
    cards_data = get_cards_data(filtered_transactions)
    exchange_rates = get_exchange_rates(user_settings["user_currencies"], api_key_currency)
    stocks_cost = get_stocks_cost(user_settings["user_stocks"], api_key_stocks)
    top_transactions = get_top_5_transactions(filtered_transactions)
    greetings = greeting()
    user_data = {
        "greeting": greetings,
        "cards": cards_data,
        "top_transactions": top_transactions,
        "exchange_rates": exchange_rates,
        "stocks": stocks_cost
    }

    return json.dumps(user_data, ensure_ascii=False, indent=4)

result = main("20.05.2020", user_choice, api_key_currency, api_key_stocks)
print(result)