"""
Тесты для модуля generators.
"""

import pytest
from typing import List, Dict, Any
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми транзакциями."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
        }
    ]


# Тесты для filter_by_currency
@pytest.mark.parametrize("currency, expected_count, expected_descriptions", [
    ("USD", 3, ["Перевод организации", "Перевод со счета на счет", "Перевод с карты на карту"]),
    ("RUB", 2, ["Перевод со счета на счет", "Перевод организации"]),
    ("EUR", 0, []),
])
def test_filter_by_currency(sample_transactions, currency, expected_count, expected_descriptions):
    """Тестирование фильтрации транзакций по валюте."""
    filtered = list(filter_by_currency(sample_transactions, currency))
    assert len(filtered) == expected_count
    descriptions = [t["description"] for t in filtered]
    assert descriptions == expected_descriptions


def test_filter_by_currency_empty_list():
    """Тестирование фильтрации с пустым списком."""
    result = list(filter_by_currency([], "USD"))
    assert result == []


def test_filter_by_currency_missing_currency_field():
    """Тестирование фильтрации с отсутствующими полями валюты."""
    transactions = [
        {"operationAmount": {"currency": {"code": "USD"}}},
        {"operationAmount": {}},
        {"description": "No currency"},
        {},
    ]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 1


def test_filter_by_currency_iterator():
    """Тестирование, что функция возвращает итератор."""
    transactions = [{"operationAmount": {"currency": {"code": "USD"}}}]
    result = filter_by_currency(transactions, "USD")
    assert hasattr(result, "__iter__")
    assert hasattr(result, "__next__")


# Тесты для transaction_descriptions
def test_transaction_descriptions(sample_transactions):
    """Тестирование получения описаний транзакций."""
    descriptions = list(transaction_descriptions(sample_transactions))
    expected = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]
    assert descriptions == expected


def test_transaction_descriptions_empty_list():
    """Тестирование генератора описаний с пустым списком."""
    result = list(transaction_descriptions([]))
    assert result == []


def test_transaction_descriptions_missing_field():
    """Тестирование генератора с отсутствующим полем description."""
    transactions = [
        {"description": "Test 1"},
        {"other": "value"},
        {},
    ]
    result = list(transaction_descriptions(transactions))
    expected = ["Test 1", "", ""]
    assert result == expected


def test_transaction_descriptions_iterator():
    """Тестирование, что функция возвращает итератор."""
    result = transaction_descriptions([{"description": "Test"}])
    assert hasattr(result, "__iter__")
    assert hasattr(result, "__next__")


# Тесты для card_number_generator
@pytest.mark.parametrize("start, stop, expected", [
    (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
    (9999999999999998, 9999999999999999, ["9999 9999 9999 9998", "9999 9999 9999 9999"]),
    (5, 5, ["0000 0000 0000 0005"]),
])
def test_card_number_generator(start, stop, expected):
    """Тестирование генерации номеров карт в диапазоне."""
    result = list(card_number_generator(start, stop))
    assert result == expected


def test_card_number_generator_format():
    """Тестирование корректного форматирования номеров карт."""
    for card_number in card_number_generator(1, 10):
        parts = card_number.split()
        assert len(parts) == 4
        assert all(len(part) == 4 for part in parts)
        assert all(c.isdigit() for part in parts for c in part)


def test_card_number_generator_invalid_range():
    """Тестирование обработки недопустимого диапазона."""
    with pytest.raises(ValueError, match="Номера карт должны быть в диапазоне от 1 до 9999999999999999"):
        list(card_number_generator(0, 5))

    with pytest.raises(ValueError, match="Номера карт должны быть в диапазоне от 1 до 9999999999999999"):
        list(card_number_generator(1, 10000000000000000))


def test_card_number_generator_start_greater_than_stop():
    """Тестирование случая, когда start > stop."""
    with pytest.raises(ValueError, match="Начальное значение не может быть больше конечного"):
        list(card_number_generator(10, 5))


def test_card_number_generator_iterator():
    """Тестирование, что функция возвращает итератор."""
    result = card_number_generator(1, 1)
    assert hasattr(result, "__iter__")
    assert hasattr(result, "__next__")