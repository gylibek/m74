# src/processing.py
from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(transactions: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    """
    Фильтрует список транзакций по заданному состоянию.

    Args:
        transactions: Список словарей с транзакциями
        state: Состояние для фильтрации (по умолчанию 'EXECUTED')

    Returns:
        Отфильтрованный список транзакций
    """
    return [item for item in transactions if item.get('state') == state]


def sort_by_date(transactions: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список транзакций по дате.

    Args:
        transactions: Список словарей с транзакциями
        descending: Если True - сортировка по убыванию (новые сверху), если False - по возрастанию

    Returns:
        Отсортированный список транзакций
    """

    def parse_date(transaction: Dict[str, Any]) -> datetime:
        """Извлекает и парсит дату из транзакции"""
        date_str = transaction.get('date', '')

        if not date_str:
            return datetime.min

        # Удаляем 'Z' в конце, если есть (UTC метка)
        if isinstance(date_str, str) and date_str.endswith('Z'):
            date_str = date_str[:-1]

        # Пробуем разные форматы дат
        formats = [
            '%Y-%m-%dT%H:%M:%S.%f',  # с микросекундами
            '%Y-%m-%dT%H:%M:%S',  # без микросекунд (ваш случай!)
            '%Y-%m-%d %H:%M:%S.%f',  # с пробелом и микросекундами
            '%Y-%m-%d %H:%M:%S',  # с пробелом без микросекунд
            '%Y-%m-%d',  # только дата
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except (ValueError, TypeError):
                continue

        # Если ни один формат не подошел, вызываем ошибку
        raise ValueError(f"Не удалось распарсить дату: {date_str}")

    return sorted(transactions, key=parse_date, reverse=descending)