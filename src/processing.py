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
        # ИСПРАВЛЕНО: используем .get() вместо прямого доступа
        date_str = transaction.get('date', '')

        if not date_str:
            return datetime.min

        # Удаляем 'Z' в конце, если есть (UTC метка)
        if isinstance(date_str, str) and date_str.endswith('Z'):
            date_str = date_str[:-1]

        # Удаляем часовой пояс, если есть (+03:00, -05:00 и т.д.)
        if isinstance(date_str, str):
            # Обрабатываем часовой пояс
            if '+' in date_str:
                date_str = date_str.split('+')[0]
            elif '-' in date_str and date_str.count('-') > 2:
                # Проверяем, что это именно часовой пояс (после даты)
                parts = date_str.rsplit('-', 1)
                if len(parts) == 2 and len(parts[1]) in [2, 5, 6]:  # -05, -05:00, -05:00:00
                    date_str = parts[0]

        # Пробуем разные форматы дат - сначала без микросекунд, потом с ними
        formats = [
            '%Y-%m-%dT%H:%M:%S',  # без микросекунд (ВАЖНО: сначала этот формат!)
            '%Y-%m-%dT%H:%M:%S.%f',  # с микросекундами
            '%Y-%m-%d %H:%M:%S',  # с пробелом без микросекунд
            '%Y-%m-%d %H:%M:%S.%f',  # с пробелом и микросекундами
            '%Y-%m-%d',  # только дата
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except (ValueError, TypeError):
                continue

        # Если ни один формат не подошел, возвращаем минимальную дату
        return datetime.min

    return sorted(transactions, key=parse_date, reverse=descending)
