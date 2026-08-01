import sys
import os

# Добавляем корень проекта и папку src в sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))  # .../homework1/tests
project_root = os.path.dirname(current_dir)              # .../homework1
src_path = os.path.join(project_root, 'src')
for path in [project_root, src_path]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Импортируем функции (пробуем разные варианты)
try:
    from generators import filter_by_currency, transaction_descriptions, card_number_generator
    print(" Импорт из generators (корень)")
except ImportError:
    try:
        from src.generators import filter_by_currency, transaction_descriptions, card_number_generator
        print(" Импорт из src.generators")
    except ImportError as e:
        print(" Не найден модуль generators ни в корне, ни в src")
        print(f"   Путь к тесту: {current_dir}")
        print(f"   Корень проекта: {project_root}")
        print(f"   Папка src: {src_path}")
        print("   Убедитесь, что файл generators.py лежит в одной из этих папок.")
        raise

import pytest
from typing import Iterator

# ==================== ФИКСТУРА С ТРАНЗАКЦИЯМИ ====================
@pytest.fixture
def sample_transactions():
    """
    Возвращает список транзакций для тестирования.
    Включает:
    - транзакции с разными валютами (USD, EUR, RUB)
    - транзакцию без описания (description=None)
    - транзакцию без поля operationAmount (проверка устойчивости)
    - транзакцию без поля description (ключ отсутствует)
    """
    return [
        {
            "id": 1,
            "description": "Перевод на карту",
            "operationAmount": {"amount": "100.00", "currency": {"name": "USD", "code": "USD"}}
        },
        {
            "id": 2,
            "description": "Оплата счета",
            "operationAmount": {"amount": "200.50", "currency": {"name": "EUR", "code": "EUR"}}
        },
        {
            "id": 3,
            "description": "Пополнение",
            "operationAmount": {"amount": "50.00", "currency": {"name": "RUB", "code": "RUB"}}
        },
        {
            "id": 4,
            "description": "Перевод на счет",
            "operationAmount": {"amount": "300.00", "currency": {"name": "USD", "code": "USD"}}
        },
        {
            "id": 5,
            "description": None,  # описание отсутствует
            "operationAmount": {"amount": "10.00", "currency": {"name": "USD", "code": "USD"}}
        },
        {
            "id": 6,
            # поле 'description' отсутствует полностью
            "operationAmount": {"amount": "20.00", "currency": {"name": "USD", "code": "USD"}}
        },
        {
            "id": 7,
            "description": "Комиссия",
            # поле 'operationAmount' отсутствует
        }
    ]

# ==================== ТЕСТЫ ДЛЯ filter_by_currency ====================
@pytest.mark.parametrize("currency_code, expected_ids", [
    ("USD", [1, 4, 5, 6]),          # четыре транзакции с USD
    ("EUR", [2]),                    # одна с EUR
    ("RUB", [3]),                    # одна с RUB
    ("GBP", []),                     # нет таких
    ("usd", []),                     # регистр важен
])
def test_filter_by_currency(sample_transactions, currency_code, expected_ids):
    """
    Проверяет, что filter_by_currency возвращает только транзакции
    с заданным кодом валюты.
    """
    result = list(filter_by_currency(sample_transactions, currency_code))
    actual_ids = [t["id"] for t in result]
    assert actual_ids == expected_ids


def test_filter_by_currency_returns_iterator(sample_transactions):
    """Проверяет, что функция возвращает итератор (генератор)."""
    gen = filter_by_currency(sample_transactions, "USD")
    assert isinstance(gen, Iterator)
    # также можно проверить, что можно вызвать next()
    first = next(gen)
    assert first["id"] == 1


def test_filter_by_currency_empty_list():
    """Пустой список транзакций → пустой итератор."""
    assert list(filter_by_currency([], "USD")) == []

# ==================== ТЕСТЫ ДЛЯ transaction_descriptions ====================
def test_transaction_descriptions(sample_transactions):
    """
    Проверяет, что генератор выдаёт описания в правильном порядке,
    заменяя отсутствующие описания на 'Описание отсутствует'.
    """
    expected = [
        "Перевод на карту",
        "Оплата счета",
        "Пополнение",
        "Перевод на счет",
        "Описание отсутствует",  # description = None
        "Описание отсутствует",  # ключа description нет
        "Комиссия",              # description есть, operationAmount отсутствует
    ]
    assert list(transaction_descriptions(sample_transactions)) == expected


def test_transaction_descriptions_empty_list():
    """Пустой список → пустой генератор."""
    assert list(transaction_descriptions([])) == []


def test_transaction_descriptions_returns_generator(sample_transactions):
    """Проверяет, что функция возвращает генератор (итератор)."""
    gen = transaction_descriptions(sample_transactions)
    assert isinstance(gen, Iterator)
    # можно вызвать next()
    first = next(gen)
    assert first == "Перевод на карту"

# ==================== ТЕСТЫ ДЛЯ card_number_generator ====================
@pytest.mark.parametrize("start, stop, expected_first, expected_last, count", [
    (1, 3, "0000 0000 0000 0001", "0000 0000 0000 0003", 3),
    (9999, 10002, "0000 0000 0000 9999", "0000 0000 0001 0002", 4),
    (0, 0, "0000 0000 0000 0000", "0000 0000 0000 0000", 1),
    (9999999999999999, 9999999999999999, "9999 9999 9999 9999", "9999 9999 9999 9999", 1),
])
def test_card_number_generator_range(start, stop, expected_first, expected_last, count):
    """
    Проверяет генерацию номеров карт в заданном диапазоне:
    - правильное количество элементов (stop - start + 1)
    - первый и последний номер соответствуют ожидаемым
    """
    numbers = list(card_number_generator(start, stop))
    assert len(numbers) == count
    assert numbers[0] == expected_first
    assert numbers[-1] == expected_last


def test_card_number_generator_format():
    """Проверяет правильность форматирования (4 группы по 4 цифры)."""
    gen = card_number_generator(5, 5)
    number = next(gen)
    groups = number.split()
    assert len(groups) == 4
    assert all(len(group) == 4 for group in groups)
    assert "".join(groups) == "0000000000000005"


def test_card_number_generator_zero_padding():
    """Проверяет дополнение ведущими нулями."""
    gen = card_number_generator(10, 10)
    assert next(gen) == "0000 0000 0000 0010"
    gen = card_number_generator(100, 100)
    assert next(gen) == "0000 0000 0000 0100"
    gen = card_number_generator(1000, 1000)
    assert next(gen) == "0000 0000 0000 1000"


def test_card_number_generator_returns_generator():
    """Проверяет, что функция возвращает генератор (итератор)."""
    gen = card_number_generator(1, 1)
    assert isinstance(gen, Iterator)
    assert next(gen) == "0000 0000 0000 0001"
