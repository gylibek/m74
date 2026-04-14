import pytest

# Импортируем модуль
from src.masks import get_mask_account, get_mask_card_number


# Тесты для функции get_mask_card_number
@pytest.mark.parametrize("card_input,expected", [
    # Тест 1: стандартный 16‑значный номер карты
    ("1234567890123456", "1234 56** **** 3456"),
    # Тест 2: номер карты ровно 16 цифр, начинающийся с нулей
    ("0012345678901234", "0012 34** **** 1234"),
    # Тест 3: строка вместо числа (должно работать аналогично)
    ("1234567890123456", "1234 56** **** 3456"),
])
def test_get_mask_card_number(card_input: str, expected: str) -> None:
    assert get_mask_card_number(card_input) == expected


@pytest.mark.parametrize("short_card,expected", [
    # Тест: номер карты короче 16 цифр — дополняем нулями слева
    ("123456789012", "0012 34** **** 9012"),
    # Тест: минимальный возможный ввод (1 цифра)
    ("1", "0000 00** **** 0001"),
])
def test_get_mask_card_number_short(short_card: str, expected: str) -> None:
    assert get_mask_card_number(short_card) == expected


@pytest.mark.parametrize("long_card,expected", [
    # Тест: ввод с большим количеством цифр (больше 16) — берём последние 16
    ("12345678901234567890", "1234 56** **** 8900"),
])
def test_get_mask_card_number_long(long_card: str, expected: str) -> None:
    assert get_mask_card_number(long_card) == expected


def test_get_mask_card_number_invalid() -> None:
    # Тест: проверка на пустую строку
    with pytest.raises(ValueError):
        get_mask_card_number("")

    # Тест: проверка на отрицательный номер карты
    with pytest.raises(ValueError):
        get_mask_card_number("-1234567890123456")


# Тесты для функции get_mask_account
@pytest.mark.parametrize("account_input,expected", [
    # Тест 1: стандартный номер счёта (больше 4 цифр)
    ("1234567890", "**7890"),
    # Тест 2: номер счёта ровно 4 цифры
    ("1234", "**1234"),
    # Тест 3: номер счёта меньше 4 цифр
    ("123", "**123"),
    ("12", "**12"),
    ("1", "**1"),
    # Тест 4: большой номер счёта
    ("123456789012345", "**345"),
    # Тест 5: строка вместо числа
    ("1234567890", "**7890"),
])
def test_get_mask_account(account_input: str, expected: str) -> None:
    assert get_mask_account(account_input) == expected


def test_get_mask_account_invalid() -> None:
    # Тест: проверка на пустую строку
    with pytest.raises(ValueError):
        get_mask_account("")

    # Тест: проверка на отрицательный номер счёта
    with pytest.raises(ValueError):
        get_mask_account("-1234567890")

    # Тест: проверка на None
    with pytest.raises(TypeError):
        get_mask_account("None")
