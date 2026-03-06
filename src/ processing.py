from datetime import datetime
from typing import List, Dict, Any

def filter_by_state(
    data: List[Dict[str, Any]],
    state: str = 'EXECUTED'
) -> List[Dict[str, Any]]:
    """
    Фильтрация данных по статусу state

    :param data: список словарей с данными
    :param state: значение состояния для фильтрации (по умолчанию 'EXECUTED')
    :return: отфильтрованный список словарей
    """
    return [item for item in data if item.get('state') == state]


def sort_by_date(
    data: List[Dict[str, Any]],
    descending: bool = True
) -> List[Dict[str, Any]]:
    """
    Сортировка данных по дате

    :param data: список словарей с данными
    :param descending: флаг сортировки (True - убывание, False - возрастание)
    :return: отсортированный список словарей
    """
    return sorted(
        data,
        key=lambda x: datetime.strptime(x['date'], '%Y-%m-%dT%H:%M:%S.%f'),
        reverse=descending
    )
