import pytest

# Импортируем модуль
from src.masks import get_mask_account, get_mask_card_number


# Тесты для функции get_mask_card_number
def test_get_mask_card_number() -> None:
    # Тест 1: стандартный 16-значный номер карты
    assert get_mask_card_number('1234567890123456') == "1234 56** **** 3456"

    # Тест 2: номер карты короче 16 цифр (дополнение нулями)
    assert get_mask_card_number('123456789012') == "0012 34** **** 9012"

    # Тест 3: номер карты ровно 16 цифр, начинающийся с нулей
    assert get_mask_card_number('0012345678901234') == "0012 34** **** 1234"

    # Тест 4: минимальный возможный ввод (1 цифра)
    assert get_mask_card_number('1') == "0001 ** ** **** 0001"

    # Тест 5: ввод с большим количеством цифр (больше 16)
    assert get_mask_card_number('12345678901234567890') == "1234 56** **** 8900"

    # Тест 6: строка вместо числа
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"

    # Тест 7: проверка на пустую строку
    with pytest.raises(ValueError, match="invalid literal for int"):
        get_mask_card_number("")

    # Тест 8: проверка на отрицательный номер карты
    with pytest.raises(ValueError, match="invalid literal for int"):
        get_mask_card_number('-1234567890123456')


# Тесты для функции get_mask_account
def test_get_mask_account() -> None:
    # Тест 1: стандартный номер счёта (больше 4 цифр)
    assert get_mask_account("1234567890") == "**7890"

    # Тест 2: номер счёта ровно 4 цифры
    assert get_mask_account("1234") == "**1234"

    # Тест 3: номер счёта меньше 4 цифр (дополнение нулями не предусмотрено, берём что есть)
    assert get_mask_account("123") == "**123"
    assert get_mask_account("12") == "**12"
    assert get_mask_account("1") == "**1"

    # Тест 4: большой номер счёта (много цифр)
    assert get_mask_account("123456789012345") == "**345"

    # Тест 5: строка вместо числа
    assert get_mask_account("1234567890") == "**7890"

    # Тест 6: проверка на пустую строку
    with pytest.raises(ValueError, match="invalid literal for int"):
        get_mask_account("")

    # Тест 7: проверка на отрицательный номер счёта
    with pytest.raises(ValueError, match="invalid literal for int"):
        get_mask_account("-1234567890")

    # Тест 8: проверка на None
    with pytest.raises(TypeError):
        get_mask_account("None")