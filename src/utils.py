# src/utils.py
import json
from typing import Any, List, Dict


def get_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл с транзакциями и возвращает список словарей.

    Аргументы:
        file_path (str): путь к файлу JSON.

    Возвращает:
        List[Dict[str, Any]]: список транзакций. Если файл пуст, повреждён,
        не является списком или не найден, возвращает пустой список.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        return []
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return []
