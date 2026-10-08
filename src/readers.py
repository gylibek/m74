"""Модуль для чтения финансовых операций из CSV- и Excel-файлов."""

import csv
from typing import Any

import pandas as pd


def read_transactions_csv(file_path: str) -> list[dict[str, Any]]:
    """Считывает финансовые операции из CSV-файла.

    Args:
        file_path: Путь к файлу CSV с транзакциями.

    Returns:
        Список словарей, где каждый словарь — одна финансовая операция.
    """
    transactions: list[dict[str, Any]] = []
    with open(file_path, encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            transactions.append(dict(row))
    return transactions


def read_transactions_excel(file_path: str) -> list[dict[str, Any]]:
    """Считывает финансовые операции из Excel-файла.

    Args:
        file_path: Путь к файлу Excel (.xlsx) с транзакциями.

    Returns:
        Список словарей, где каждый словарь — одна финансовая операция.
    """
    dataframe = pd.read_excel(file_path)
    records = dataframe.to_dict(orient="records")
    return [{str(key): value for key, value in record.items()} for record in records]
