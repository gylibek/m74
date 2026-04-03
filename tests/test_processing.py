from datetime import datetime
from typing import Any, Dict, List

import pytest
from processing import filter_by_state, sort_by_date

from src import processing


# Фикстура для создания тестовых данных
@pytest.fixture
def test_data() -> List[Dict[str, Any]]:
    return [
        {
            'id': 1,
            'date': '2026-03-25T12:00:00.000000',
            'state': 'EXECUTED',
            'amount': 1000
        },
        {
            'id': 2,
            'date': '2026-03-24T12:00:00.000000',
            'state': 'PENDING',
            'amount': 2000
        },
        {
            'id': 3,
            'date': '2026-03-26T12:00:00.000000',
            'state': 'EXECUTED',
            'amount': 3000
        },
        {
            'id': 4,
            'date': '2026-03-25T12:00:00.000000',
            'state': 'CANCELLED',
            'amount': 4000
        }
    ]


# --- Тесты для функции filter_by_state ---

def test_filter_by_state_default(test_data: List[Dict[str, Any]]) -> None:
    """Тест фильтрации по умолчанию (state='EXECUTED')"""
    result = filter_by_state(test_data)
    assert len(result) == 2
    assert all(item['state'] == 'EXECUTED' for item in result)


def test_filter_by_state_custom_state(test_data: List[Dict[str, Any]]) -> None:
    """Тест фильтрации с указанием состояния 'PENDING'"""
    result = filter_by_state(test_data, 'PENDING')
    assert len(result) == 1
    assert result[0]['state'] == 'PENDING'


def test_filter_by_state_empty_list() -> None:
    """Тест с пустым списком данных"""
    result = filter_by_state([])
    assert result == []


def test_filter_by_state_no_matching_state(test_data: List[Dict[str, Any]]) -> None:
    """Тест, когда нет элементов с указанным состоянием"""
    result = filter_by_state(test_data, 'UNKNOWN')
    assert result == []


def test_filter_by_state_missing_state_key(test_data: List[Dict[str, Any]]) -> None:
    """Тест обработки элементов без ключа 'state'"""
    data_with_missing = test_data + [{'id': 5, 'date': '2026-03-27T12:00:00.000000'}]
    result = filter_by_state(data_with_missing, 'EXECUTED')
    assert len(result) == 2  # Должно остаться 2 элемента с 'EXECUTED'


# Параметризованные тесты для filter_by_state
@pytest.mark.parametrize(
    "state,expected_count",
    [
        ('EXECUTED', 2),
        ('PENDING', 1),
        ('CANCELLED', 1),
        ('UNKNOWN', 0),
        ('', 0)
    ]
)
def test_filter_by_state_parametrized(
    test_data: List[Dict[str, Any]],
    state: str,
    expected_count: int
) -> None:
    """Параметризованный тест для разных состояний"""
    result = filter_by_state(test_data, state)
    assert len(result) == expected_count


# --- Тесты для функции sort_by_date ---

def test_sort_by_date_descending(test_data: List[Dict[str, Any]]) -> None:
    """Тест сортировки по убыванию (по умолчанию)"""
    sorted_data = sort_by_date(test_data)
    dates = [
        datetime.strptime(item['date'], '%Y-%m-%dT%H:%M:%S.%f')
        for item in sorted_data
    ]
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_ascending(test_data: List[Dict[str, Any]]) -> None:
    """Тест сортировки по возрастанию"""
    sorted_data = sort_by_date(test_data, descending=False)
    dates = [
        datetime.strptime(item['date'], '%Y-%m-%dT%H:%M:%S.%f')
        for item in sorted_data
    ]
    assert dates == sorted(dates)


def test_sort_by_date_empty_list() -> None:
    """Тест сортировки пустого списка"""
    assert sort_by_date([]) == []


def test_sort_by_date_single_element() -> None:
    """Тест сортировки списка с одним элементом"""
    single_item = [{'date': '2026-03-25T12:00:00.000000', 'id': 1}]
    result = sort_by_date(single_item)
    assert result == single_item


def test_sort_by_date_same_dates() -> None:
    """Тест сортировки элементов с одинаковыми датами"""
    data = [
        {'date': '2026-03-25T12:00:00.000000', 'id': 1},
        {'date': '2026-03-25T12:00:00.000000', 'id': 2}
    ]
    original_order = [item['id'] for item in data]
    sorted_data = sort_by_date(data)
    sorted_order = [item['id'] for item in sorted_data]
    assert sorted_order == original_order  # Порядок должен сохраниться


def test_sort_by_date_invalid_format() -> None:
    """Тест обработки некорректного формата даты"""
    invalid_data = [{'date': 'INVALID_DATE_FORMAT'}]
    with pytest.raises(ValueError):
        sort_by_date(invalid_data)
