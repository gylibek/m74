# tests/test_processing.py
from typing import Any, Dict, List
from src.processing import filter_by_state, sort_by_date


def test_filter_by_state() -> None:
    transactions: List[Dict[str, Any]] = [
        {'state': 'EXECUTED', 'amount': 100},
        {'state': 'PENDING', 'amount': 200},
        {'state': 'EXECUTED', 'amount': 300},
    ]

    result = filter_by_state(transactions)
    assert len(result) == 2
    assert all(item['state'] == 'EXECUTED' for item in result)


def test_filter_by_state_with_custom_state() -> None:
    transactions: List[Dict[str, Any]] = [
        {'state': 'EXECUTED', 'amount': 100},
        {'state': 'PENDING', 'amount': 200},
        {'state': 'CANCELED', 'amount': 300},
    ]

    result = filter_by_state(transactions, state='PENDING')
    assert len(result) == 1
    assert result[0]['state'] == 'PENDING'


def test_filter_by_state_empty_list() -> None:
    assert filter_by_state([]) == []


def test_sort_by_date_descending() -> None:
    transactions: List[Dict[str, Any]] = [
        {'date': '2023-01-15T10:30:00', 'amount': 100},
        {'date': '2023-01-20T10:30:00', 'amount': 200},
        {'date': '2023-01-10T10:30:00', 'amount': 300},
    ]

    result = sort_by_date(transactions, descending=True)
    assert result[0]['date'] == '2023-01-20T10:30:00'
    assert result[1]['date'] == '2023-01-15T10:30:00'
    assert result[2]['date'] == '2023-01-10T10:30:00'


def test_sort_by_date_ascending() -> None:
    transactions: List[Dict[str, Any]] = [
        {'date': '2023-01-15T10:30:00', 'amount': 100},
        {'date': '2023-01-20T10:30:00', 'amount': 200},
        {'date': '2023-01-10T10:30:00', 'amount': 300},
    ]

    result = sort_by_date(transactions, descending=False)
    assert result[0]['date'] == '2023-01-10T10:30:00'
    assert result[1]['date'] == '2023-01-15T10:30:00'
    assert result[2]['date'] == '2023-01-20T10:30:00'


def test_sort_by_date_with_missing_date() -> None:
    transactions: List[Dict[str, Any]] = [
        {'amount': 100},  # без даты
        {'date': '2023-01-20T10:30:00', 'amount': 200},
        {'date': '2023-01-10T10:30:00', 'amount': 300},
    ]

    result = sort_by_date(transactions, descending=True)
    # Транзакции без даты должны быть в конце
    assert result[-1].get('date') is None
