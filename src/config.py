import os

from dotenv import load_dotenv

from src.utils import get_data_from_xlsx

load_dotenv()
api_key_currency = os.getenv("API_KEY_CURRENCY")
api_key_stocks = os.getenv("API_KEY_STOCKS")
input_date_str = "20.03.2020"
transactions = get_data_from_xlsx(r'../data/operations.xls')
year = 2020
month = 5
date = "2020.05"
limit = 50
search = "Перевод"
