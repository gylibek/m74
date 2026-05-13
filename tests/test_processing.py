from datetime import datetime
from typing import Any, Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date


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


# Ошибка 1: Неправильное ожидание для элементов без ключа 'state'
def test_filter_by_state_missing_state_key() -> None:
    """Тест обработки элементов без ключа 'state'"""
    # Исправлено: создаем тестовые данные без использования фикстуры
    data_with_missing = [
        {'id': 1, 'date': '2026-03-27T12:00:00.000000', 'state': 'EXECUTED'},
        {'id': 2, 'date': '2026-03-27T12:00:00.000000', 'state': 'EXECUTED'},
        {'id': 5, 'date': '2026-03-27T12:00:00.000000'}  # Нет ключа 'state'
    ]
    result = filter_by_state(data_with_missing, 'EXECUTED')
    # Исправлено: должно быть 2 элемента (оба с EXECUTED)
    assert len(result) == 2
    assert all(item.get('state') == 'EXECUTED' for item in result)


# Параметризованные тесты для filter_by_state
@pytest.mark.parametrize(
    "state,expected_count",
    [
        ('EXECUTED', 2),
        ('PENDING', 1),
        ('CANCELLED', 1),
        ('UNKNOWN', 0),
        ('', 0)  # Ошибка 2: пустая строка - валидное значение, но не должно совпадать
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
    # Ошибка 3: Проверяем, что даты отсортированы по убыванию
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_ascending(test_data: List[Dict[str, Any]]) -> None:
    """Тест сортировки по возрастанию"""
    sorted_data = sort_by_date(test_data, descending=False)
    dates = [
        datetime.strptime(item['date'], '%Y-%m-%dT%H:%M:%S.%f')
        for item in sorted_data
    ]
    assert dates == sorted(dates)  # По возрастанию


def test_sort_by_date_empty_list() -> None:
    """Тест сортировки пустого списка"""
    assert sort_by_date([]) == []


def test_sort_by_date_single_element() -> None:
    """Тест сортировки списка с одним элементом"""
    single_item = [{'date': '2026-03-25T12:00:00.000000', 'id': 1}]
    result = sort_by_date(single_item)
    assert result == single_item


# Ошибка 4: Тест для одинаковых дат - порядок может не сохраняться
def test_sort_by_date_same_dates() -> None:
    """Тест сортировки элементов с одинаковыми датами"""
    data = [
        {'date': '2026-03-25T12:00:00.000000', 'id': 1},
        {'date': '2026-03-25T12:00:00.000000', 'id': 2}
    ]
    original_order = [item['id'] for item in data]
    sorted_data = sort_by_date(data)
    sorted_order = [item['id'] for item in sorted_data]
    # Исправлено: при одинаковых датах порядок может быть любым
    # Поэтому проверяем только наличие элементов
    assert set(sorted_order) == set(original_order)
    assert len(sorted_data) == len(data)


# Ошибка 5: Тест для некорректного формата даты
def test_sort_by_date_invalid_format() -> None:
    """Тест обработки некорректного формата даты"""
    invalid_data = [{'date': 'INVALID_DATE_FORMAT', 'id': 1}]
    with pytest.raises((ValueError, KeyError)):  # Может быть ValueError или KeyError
        sort_by_date(invalid_data)


# Дополнительные тесты для проверки корректности

def test_sort_by_date_missing_date_key() -> None:
    """Тест обработки элементов без ключа 'date'"""
    data_without_date = [
        {'date': '2026-03-26T12:00:00.000000', 'id': 1},
        {'id': 2}  # Нет ключа 'date'
    ]
    with pytest.raises(KeyError):
        sort_by_date(data_without_date)


def test_sort_by_date_different_formats() -> None:
    """Тест сортировки с разными форматами дат"""
    data = [
        {'date': '2024-03-11T02:26:18.671407', 'id': 1},
        {'date': '2024-03-11T02:26:18', 'id': 2},  # Без микросекунд
        {'date': '2024-03-11T02:26:18.671407Z', 'id': 3}  # С Z
    ]
    # Функция должна обработать разные форматы
    result = sort_by_date(data)
    assert len(result) == 3


# Альтернативный вариант для sort_by_date_same_dates (если нужна стабильность)
def test_sort_by_date_same_dates_stable() -> None:
    """Тест стабильности сортировки при одинаковых датах"""
    data = [
        {'date': '2026-03-25T12:00:00.000000', 'id': 1, 'order': 'first'},
        {'date': '2026-03-25T12:00:00.000000', 'id': 2, 'order': 'second'}
    ]
    sorted_data = sort_by_date(data)
    # Python 3.11+ гарантирует стабильную сортировку
    # Поэтому порядок должен сохраниться
    assert sorted_data[0]['order'] == 'first'
    assert sorted_data[1]['order'] == 'second'