# tests/test_processing.py
from typing import Any, Dict, List
from src.processing import filter_by_state, sort_by_date


def test_filter_by_state() -> None:
    """Тест фильтрации транзакций по состоянию EXECUTED"""
    transactions: List[Dict[str, Any]] = [
        {'state': 'EXECUTED', 'amount': 100},
        {'state': 'PENDING', 'amount': 200},
        {'state': 'EXECUTED', 'amount': 300},
    ]

    result = filter_by_state(transactions)
    assert len(result) == 2
    assert all(item['state'] == 'EXECUTED' for item in result)


def test_filter_by_state_with_custom_state() -> None:
    """Тест фильтрации транзакций с пользовательским состоянием"""
    transactions: List[Dict[str, Any]] = [
        {'state': 'EXECUTED', 'amount': 100},
        {'state': 'PENDING', 'amount': 200},
        {'state': 'CANCELED', 'amount': 300},
    ]

    result = filter_by_state(transactions, state='PENDING')
    assert len(result) == 1
    assert result[0]['state'] == 'PENDING'


def test_filter_by_state_empty_list() -> None:
    """Тест фильтрации пустого списка"""
    assert filter_by_state([]) == []


def test_filter_by_state_no_matching() -> None:
    """Тест, когда нет транзакций с указанным состоянием"""
    transactions: List[Dict[str, Any]] = [
        {'state': 'PENDING', 'amount': 100},
        {'state': 'PENDING', 'amount': 200},
    ]

    result = filter_by_state(transactions, state='EXECUTED')
    assert len(result) == 0


def test_sort_by_date_descending() -> None:
    """Тест сортировки по дате по убыванию (новые сверху)"""
    transactions: List[Dict[str, Any]] = [
        {'date': '2023-01-15T10:30:00.000', 'amount': 100},
        {'date': '2023-01-20T10:30:00.000', 'amount': 200},
        {'date': '2023-01-10T10:30:00.000', 'amount': 300},
    ]

    result = sort_by_date(transactions, descending=True)
    assert result[0]['date'] == '2023-01-20T10:30:00.000'
    assert result[1]['date'] == '2023-01-15T10:30:00.000'
    assert result[2]['date'] == '2023-01-10T10:30:00.000'


def test_sort_by_date_ascending() -> None:
    """Тест сортировки по дате по возрастанию (старые сверху)"""
    transactions: List[Dict[str, Any]] = [
        {'date': '2023-01-15T10:30:00.000', 'amount': 100},
        {'date': '2023-01-20T10:30:00.000', 'amount': 200},
        {'date': '2023-01-10T10:30:00.000', 'amount': 300},
    ]

    result = sort_by_date(transactions, descending=False)
    assert result[0]['date'] == '2023-01-10T10:30:00.000'
    assert result[1]['date'] == '2023-01-15T10:30:00.000'
    assert result[2]['date'] == '2023-01-20T10:30:00.000'


def test_sort_by_date_without_microseconds() -> None:
    """Тест сортировки с датами без микросекунд"""
    transactions: List[Dict[str, Any]] = [
        {'date': '2023-01-15T10:30:00', 'amount': 100},
        {'date': '2023-01-20T10:30:00', 'amount': 200},
        {'date': '2023-01-10T10:30:00', 'amount': 300},
    ]

    result = sort_by_date(transactions, descending=True)
    # Проверяем порядок, а не точное значение
    dates = [item['date'] for item in result]
    assert dates[0] == '2023-01-20T10:30:00'
    assert dates[1] == '2023-01-15T10:30:00'
    assert dates[2] == '2023-01-10T10:30:00'


def test_sort_by_date_with_missing_date() -> None:
    """Тест сортировки с транзакцией без даты"""
    transactions: List[Dict[str, Any]] = [
        {'amount': 100},  # без даты
        {'date': '2023-01-20T10:30:00.000', 'amount': 200},
        {'date': '2023-01-10T10:30:00.000', 'amount': 300},
    ]

    result = sort_by_date(transactions, descending=True)
    # Проверяем, что последняя транзакция - без даты
    assert result[-1].get('date') is None
    # Проверяем, что остальные отсортированы правильно
    assert result[0]['date'] == '2023-01-20T10:30:00.000'
    assert result[1]['date'] == '2023-01-10T10:30:00.000'


def test_sort_by_date_all_missing_dates() -> None:
    """Тест сортировки, когда у всех транзакций нет даты"""
    transactions: List[Dict[str, Any]] = [
        {'amount': 100},
        {'amount': 200},
        {'amount': 300},
    ]

    result = sort_by_date(transactions, descending=True)
    assert len(result) == 3
    # Все транзакции без даты должны остаться на своих местах
    for item in result:
        assert item.get('date') is None
