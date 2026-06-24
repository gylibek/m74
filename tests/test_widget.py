# tests/test_widget.py
import pytest
from src.widget import get_date, mask_account_card


def test_mask_account_card_credit_card() -> None:
    """Тестируем маскировку для кредитных карт (Visa, Maestro и т.д.)"""
    assert mask_account_card("Visa Platinum 7000792289606361") == "Visa Platinum 7000 79** **** 6361"
    assert mask_account_card("Maestro 7000792289606361") == "Maestro 7000 79** **** 6361"


def test_mask_account_card_account() -> None:
    """Тестируем маскировку для банковских счетов"""
    assert mask_account_card("Счет 73654108430135874305") == "Счет **4305"


def test_mask_account_card_edge_cases() -> None:
    """Тестируем крайние случаи и граничные условия"""
    assert mask_account_card("Visa 1234567890123456") == "Visa 1234 56** **** 3456"
    assert mask_account_card("Счет 123456789012345678901234567890") == "Счет **7890"


def test_mask_account_card_invalid_format() -> None:
    """Тестируем обработку некорректного формата входной строки"""
    # ИСПРАВЛЕНО: проверяем, что функция выбрасывает ValueError для некорректных данных
    invalid_inputs = [
        "7000792289606361",  # Нет типа карты/счёта
        "Visa",  # Нет номера карты/счёта
        "",  # Пустая строка
        "   ",  # Только пробелы
        "Invalid Type",  # Только тип без номера
        "123",  # Только цифры без типа
    ]

    for invalid_input in invalid_inputs:
        with pytest.raises(ValueError):
            mask_account_card(invalid_input)


def test_mask_account_card_whitespace() -> None:
    """Тестируем обработку лишних пробелов"""
    assert mask_account_card("Visa   Platinum  7000792289606361") == "Visa Platinum 7000 79** **** 6361"
    assert mask_account_card(" Счет  73654108430135874305") == "Счет **4305"


def test_mask_account_card_with_different_card_names() -> None:
    """Тестируем различные названия карт"""
    assert mask_account_card("Visa Classic 1234567890123456") == "Visa Classic 1234 56** **** 3456"
    assert mask_account_card("MasterCard Gold 1234567890123456") == "MasterCard Gold 1234 56** **** 3456"
    assert mask_account_card("American Express 1234567890123456") == "American Express 1234 56** **** 3456"


def test_mask_account_card_with_account_variants() -> None:
    """Тестируем различные варианты написания счета"""
    assert mask_account_card("Счет 12345678901234567890") == "Счет **7890"
    assert mask_account_card("Счет 1234567890") == "Счет **7890"  # Короткий счет


def test_get_date_standard_format() -> None:
    """Тестируем стандартный ISO-формат даты"""
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"
    assert get_date("2023-12-25T23:59:59.999999") == "25.12.2023"


def test_get_date_utc_format() -> None:
    """Тестируем формат с UTC (Z в конце)"""
    assert get_date("2024-03-11T02:26:18.671407Z") == "11.03.2024"


def test_get_date_edge_cases() -> None:
    """Тестируем крайние случаи для даты"""
    min_date_str = "0001-01-01T00:00:00"
    assert get_date(min_date_str) == "01.01.0001"

    max_date_str = "9999-12-31T23:59:59.999999"
    assert get_date(max_date_str) == "31.12.9999"


def test_get_date_invalid_format() -> None:
    """Тестируем обработку некорректного формата даты"""
    with pytest.raises(ValueError):
        get_date("2024-03-32T02:26:18.671407")  # Некорректный день месяца

    with pytest.raises(ValueError):
        get_date("invalid-date")  # Некорректный формат строки

    with pytest.raises(ValueError):
        get_date("")  # Пустая строка


def test_get_date_timezone() -> None:
    """Тестируем обработку строк с часовым поясом"""
    assert get_date("2024-03-11T02:26:18.671407+03:00") == "11.03.2024"
    assert get_date("2024-03-11T02:26:18.671407-05:00") == "11.03.2024"
