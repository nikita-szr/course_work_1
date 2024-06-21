import pandas as pd
from typing import Optional
from datetime import datetime, timedelta
import json
import functools


# дата гггг.мм.дд
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> str:
    """Функция возвращает траты по заданной категории за последние три месяца
    (от переданной даты, если дата не передана берет текущую)"""
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], format='%d.%m.%Y %H:%M:%S')
    if date is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date, '%Y.%m.%d')
    start_date = date - timedelta(days=date.day - 1) - timedelta(days=3 * 30)
    filtered_transactions = transactions[(transactions['Дата операции'] >= start_date) &
                                         (transactions['Дата операции'] <= date) &
                                         (transactions['Категория'] == category)]
    grouped_transactions = filtered_transactions.groupby(pd.Grouper(key='Дата операции', freq='ME')).sum()
    return json.dumps(grouped_transactions, ensure_ascii=False, indent=4)


def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> str:
    """Функция возвращает средние траты в каждый из дней недели за последние три месяца (от переданной даты)"""
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], format='%d.%m.%Y %H:%M:%S')
    if date is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date, '%Y.%m.%d')
    start_date = date - timedelta(days=date.day) - timedelta(days=3 * 30)
    filtered_transactions = transactions[(transactions['Дата операции'] >= start_date) &
                                         (transactions['Дата операции'] <= date)]
    filtered_transactions = filtered_transactions.copy()
    filtered_transactions.loc[:, 'День недели'] = filtered_transactions['Дата операции'].dt.dayofweek
    grouped_transactions = filtered_transactions.groupby('День недели')['Сумма операции'].mean()
    weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    grouped_transactions.index = weekdays
    return json.dumps(grouped_transactions, ensure_ascii=False, indent=4)


def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> str:
    """Функция выводит средние траты в рабочий и в выходной день за последние три месяца (от переданной даты)."""
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], format='%d.%m.%Y %H:%M:%S')
    if date is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date, '%Y.%m.%d')
    weekend_days = [5, 6]
    start_date = date - timedelta(days=date.day) - timedelta(days=3 * 30)
    filtered_transactions = transactions[(transactions['Дата операции'] >= start_date) &
                                         (transactions['Дата операции'] <= date)]
    filtered_transactions = filtered_transactions.copy()
    filtered_transactions['День недели'] = filtered_transactions['Дата операции'].dt.dayofweek
    filtered_transactions['Тип дня'] = 'Рабочий'
    filtered_transactions.loc[filtered_transactions['День недели'].isin(weekend_days), 'Тип дня'] = 'Выходной'
    grouped_transactions = filtered_transactions.groupby('Тип дня')['Сумма операции'].mean()
    return json.dumps(grouped_transactions, ensure_ascii=False, indent=4)


def report_to_file_default(func):
    """Записывает в файл результат, который возвращает функция, формирующая отчет."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        with open("function_operation_report.txt", "w") as file:
            file.write(str(result))
        return result
    return wrapper


def report_to_file(filename="function_operation_report.txt"):
    """Записывает в переданный файл результат, который возвращает функция, формирующая отчет."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(filename, "w") as file:
                file.write(str(result))
            return result
        return wrapper
    return decorator


# спросить у преподов почему в примере функции должны возвращать pd.dataframe,
# а в критериях оценки показано что возвращать надо json
