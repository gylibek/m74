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
    print("✅ Импорт из generators (корень)")
except ImportError:
    try:
        from src.generators import filter_by_currency, transaction_descriptions, card_number_generator
        print("✅ Импорт из src.generators")
    except ImportError as e:
        print("❌ Не найден модуль generators ни в корне, ни в src")
        print(f"   Путь к тесту: {current_dir}")
        print(f"   Корень проекта: {project_root}")
        print(f"   Папка src: {src_path}")
        print("   Убедитесь, что файл generators.py лежит в одной из этих папок.")
        raise

import pytest

# ==================== ТЕСТОВЫЕ ДАННЫЕ ====================
TEST_TRANSACTIONS = [
    {
        "id": 1,
        "description": "Перевод на карту",
        "operationAmount": {
            "amount": "100.00",
            "currency": {"name": "USD", "code": "USD"}
        }
    },
    {
        "id": 2,
        "description": "Оплата счета",
        "operationAmount": {
            "amount": "200.50",
            "currency": {"name": "EUR", "code": "EUR"}
        }
    },
    {
        "id": 3,
        "description": "Пополнение",
        "operationAmount": {
            "amount": "50.00",
            "currency": {"name": "RUB", "code": "RUB"}
        }
    },
    {
        "id": 4,
        "description": "Перевод на счет",
        "operationAmount": {
            "amount": "300.00",
            "currency": {"name": "USD", "code": "USD"}
        }
    },
    {
        "id": 5,
        "description": "Комиссия",
        # operationAmount отсутствует
    }
]


# ==================== ТЕСТЫ ДЛЯ filter_by_currency ====================
def test_filter_by_currency_usd():
    usd_transactions = list(filter_by_currency(TEST_TRANSACTIONS, "USD"))
    assert len(usd_transactions) == 2
    assert all(t["operationAmount"]["currency"]["code"] == "USD" for t in usd_transactions)
    ids = [t["id"] for t in usd_transactions]
    assert ids == [1, 4]


def test_filter_by_currency_eur():
    eur_transactions = list(filter_by_currency(TEST_TRANSACTIONS, "EUR"))
    assert len(eur_transactions) == 1
    assert eur_transactions[0]["id"] == 2


def test_filter_by_currency_no_result():
    gbp_transactions = list(filter_by_currency(TEST_TRANSACTIONS, "GBP"))
    assert gbp_transactions == []


def test_filter_by_currency_missing_operation_amount():
    usd_transactions = list(filter_by_currency(TEST_TRANSACTIONS, "USD"))
    ids = [t["id"] for t in usd_transactions]
    assert ids == [1, 4]  # id=5 игнорируется


TEST_TRANSACTIONS = [
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
        # "description" отсутствует – проверяем заглушку
        # operationAmount отсутствует – проверяем устойчивость
    }
]

# ==================== ТЕСТЫ ДЛЯ card_number_generator ====================
def test_card_number_generator_single():
    numbers = list(card_number_generator(1, 1))
    assert numbers == ["0000 0000 0000 0001"]


def test_card_number_generator_range():
    numbers = list(card_number_generator(9999999999999999, 10000000000000000))
    expected = [
        "9999 9999 9999 9999",
        "1000 0000 0000 0000"
    ]
    assert numbers == expected


def test_card_number_generator_format():
    gen = card_number_generator(5, 5)
    number = next(gen)
    assert len(number.replace(" ", "")) == 16
    assert number == "0000 0000 0000 0005"


def test_card_number_generator_zero():
    gen = card_number_generator(0, 0)
    assert next(gen) == "0000 0000 0000 0000"