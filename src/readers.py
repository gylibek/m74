
"""Модуль для чтения финансовых операций из JSON-, CSV- и Excel-файлов."""

import csv
import json
from typing import Any, cast

import pandas as pd


def read_transactions_json(file_path: str) -> list[dict[str, Any]]:
    """Считывает финансовые операции из JSON-файла.

    Args:
        file_path: Путь к файлу JSON с транзакциями.

    Returns:
        Список словарей с банковскими операциями.
    """
    with open(file_path, encoding="utf-8") as json_file:
        data = json.load(json_file)
    return cast(list[dict[str, Any]], data)


def read_transactions_csv(file_path: str) -> list[dict[str, Any]]:
    """Считывает финансовые операции из CSV-файла.

    Args:
        file_path: Путь к файлу CSV с транзакциями.

    Returns:
        Список словарей с банковскими операциями.
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
        Список словарей с банковскими операциями.
    """
    dataframe = pd.read_excel(file_path)
    records = dataframe.to_dict(orient="records")
    return [{str(k): v for k, v in rec.items()} for rec in records]
