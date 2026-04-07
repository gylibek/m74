from datetime import datetime


import pytest
from your_module import get_date, mask_account_card  # замените your_module на имя вашего модуля


# Тесты для функции mask_account_card
def test_mask_account_card_credit_card():
    """Тестируем маскировку для кредитных карт (Visa, Maestro и т.д.)"""
    assert mask_account_card("Visa Platinum 7000792289606361") == "Visa Platinum XXXX XXXX XXXX 6361"
    assert mask_account_card("Maestro 7000792289606361") == "Maestro XXXX XXXX XXXX 6361"


def test_mask_account_card_account():
    """Тестируем маскировку для банковских счетов"""
    assert mask_account_card("Счет 73654108430135874305") == "Счет XXXX XXXX XXXX 3015"


def test_mask_account_card_edge_cases():
    """Тестируем крайние случаи и граничные условия"""
    # Короткий номер карты
    assert mask_account_card("Visa 1234567890123456") == "Visa XXXX XXXX XXXX 3456"
    # Очень длинный номер счёта
    assert mask_account_card("Счет 123456789012345678901234567890") == "Счет XXXX XXXX XXXX 7890"


def test_mask_account_card_invalid_format():
    """Тестируем обработку некорректного формата входной строки"""
    with pytest.raises(ValueError):
        mask_account_card("7000792289606361")  # Нет типа карты/счёта
    with pytest.raises(ValueError):
        mask_account_card("Visa")  # Нет номера карты/счёта
    with pytest.raises(ValueError):
        mask_account_card("Invalid Type 1234567890123456")  # Неподдерживаемый тип


def test_mask_account_card_whitespace():
    """Тестируем обработку лишних пробелов"""
    assert mask_account_card("Visa   Platinum  7000792289606361") == "Visa Platinum XXXX XXXX XXXX 6361"
    assert mask_account_card(" Счет  73654108430135874305") == "Счет XXXX XXXX XXXX 3015"


# Тесты для функции get_date
def test_get_date_standard_format():
    """Тестируем стандартный ISO-формат даты"""
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"
    assert get_date("2023-12-25T23:59:59.999999") == "25.12.2023"


def test_get_date_utc_format():
    """Тестируем формат с UTC (Z в конце)"""
    assert get_date("2024-03-11T02:26:18.671407Z") == "11.03.2024"


def test_get_date_edge_cases():
    """Тестируем крайние случаи для даты"""
    # Минимальная дата, поддерживаемая datetime
    min_date = datetime.min.isoformat().replace('+00:00', 'Z')
    assert get_date(min_date) == "01.01.0001"

    # Максимальная дата, поддерживаемая datetime
    max_date = datetime.max.isoformat().replace('+00:00', 'Z')
    assert get_date(max_date) == "31.12.9999"


def test_get_date_invalid_format():
    """Тестируем обработку некорректного формата даты"""
    with pytest.raises(ValueError):
        get_date("2024-03-32T02:26:18.671407")  # Некорректный день месяца
    with pytest.raises(ValueError):
        get_date("invalid-date")  # Некорректный формат строки
    with pytest.raises(ValueError):
        get_date("")  # Пустая строка


def test_get_date_timezone():
    """Тестируем обработку строк с часовым поясом"""
    assert get_date("2024-03-11T02:26:18.671407+03:00") == "11.03.2024"
    assert get_date("2024-03-11T02:26:18.671407-05:00") == "11.03.2024"
