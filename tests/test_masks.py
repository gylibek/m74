from src import widget

# Импортируем модуль


# Пример использования функций
def main() -> None:

    # Тестовые данные для маскировки
    card_input = "Visa Platinum 7000792289606361"
    masked_card = widget.mask_account_card(card_input)
    print(f"Исходная карта: {card_input}")
    print(f"Замаскированная карта: {masked_card}")
    # Тестовые данные для даты
    date_input = "2024-03-11T02:26:18.671407"
    formatted_date = widget.get_date(date_input)
    print(f"\nИсходная дата: {date_input}")
    print(f"Форматированная дата: {formatted_date}")


if __name__ == "__main__":
    main()


def display_results() -> None:
    # Пример с форматированием
    card_examples = [
        "Visa Platinum 7000792289606361",
        "Maestro 7000792289606361",
        "Счет 73654108430135874305"
    ]

    date_examples = [
        "2024-03-11T02:26:18.671407",
        "2023-12-25T23:59:59.999999",
        "2025-01-01T00:00:00.000000"
    ]

    print("Результаты работы функции маскировки:")
    print("-------------------------------------")
    for card in card_examples:
        print(f"Исходная: {card}")
        print(f"Результат: {widget.mask_account_card(card)}\n")

    print("Результаты работы функции форматирования даты:")
    print("---------------------------------------------")
    for date in date_examples:
        print(f"Исходная: {date}")
        print(f"Результат: {widget.get_date(date)}\n")


if __name__ == "__main__":
    display_results()

import pytest

# Тесты для функции get_mask_card_number
def test_get_mask_card_number():
    # Тест 1: стандартный 16-значный номер карты
    assert get_mask_card_number(1234567890123456) == "1234 56** **** 3456"

    # Тест 2: номер карты короче 16 цифр (дополнение нулями)
    assert get_mask_card_number(123456789012) == "0012 34** **** 9012"

    # Тест 3: номер карты ровно 16 цифр, начинающийся с нулей
    assert get_mask_card_number(0012345678901234) == "0012 34** **** 1234"

    # Тест 4: минимальный возможный ввод (1 цифра)
    assert get_mask_card_number(1) == "0001 ** ** **** 0001"

    # Тест 5: ввод с большим количеством цифр (больше 16)
    assert get_mask_card_number(12345678901234567890) == "1234 56** **** 8900"

    # Тест 6: строка вместо числа (должна корректно обрабатываться, т.к. функция преобразует в строку)
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"

    # Тест 7: проверка на пустую строку
    with pytest.raises(ValueError, match="invalid literal for int"):
        get_mask_card_number("")

    # Тест 8: проверка на отрицательный номер карты
    with pytest.raises(ValueError, match="invalid literal for int"):
        get_mask_card_number(-1234567890123456)


# Тесты для функции get_mask_account
def test_get_mask_account():
    # Тест 1: стандартный номер счёта (больше 4 цифр)
    assert get_mask_account(1234567890) == "**7890"

    # Тест 2: номер счёта ровно 4 цифры
    assert get_mask_account(1234) == "**1234"

    # Тест 3: номер счёта меньше 4 цифр (дополнение нулями не предусмотрено, берём что есть)
    assert get_mask_account(123) == "**123"
    assert get_mask_account(12) == "**12"
    assert get_mask_account(1) == "**1"

    # Тест 4: большой номер счёта (много цифр)
    assert get_mask_account(123456789012345) == "**345"

    # Тест 5: строка вместо числа (должна корректно обрабатываться, т.к. функция преобразует в строку)
    assert get_mask_account("1234567890") == "**7890"

    # Тест 6: проверка на пустую строку
    with pytest.raises(ValueError, match="invalid literal for int"):
        get_mask_account("")

    # Тест 7: проверка на отрицательный номер счёта
    with pytest.raises(ValueError, match="invalid literal for int"):
        get_mask_account(-1234567890)

    # Тест 8: проверка на None
    with pytest.raises(TypeError):
        get_mask_account(None)
