from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number

card_examples = [
    "Visa Platinum 7000792289606361",
    "Maestro 7000792289606361",
    "Счет 73654108430135874305"
]


def mask_account_card(card: str) -> str:
    """
       Маскирует номер банковской карты или счета в зависимости от типа.
    Маскирует номер банковской карты или счета в зависимости от типа.

       Функция принимает строку с типом карты/счета и номером,
       разделенными пробелом, и возвращает строку с замаскированным номером.
       Для карт и счетов используются разные типы маскировки.
    Функция принимает строку с типом карты/счета и номером,
    разделенными пробелом, и возвращает строку с замаскированным номером.
    Для карт и счетов используются разные типы маскировки.

       Параметры:
       input_string (str): входная строка с типом и номером карты/счета
           Допустимые форматы:
           - "Visa Platinum 7000792289606361"
           - "Maestro 7000792289606361"
           - "Счет 73654108430135874305"
    Параметры:
    input_string (str): входная строка с типом и номером карты/счета
        Допустимые форматы:
        - "Visa Platinum 7000792289606361"
        - "Maestro 7000792289606361"
        - "Счет 73654108430135874305"

    Возвращает:
    str: строка с замаскированным номером карты/счета

       Возвращает:
       str: строка с замаскированным номером карты/счета
    Примеры использования:
    >>> mask_account_card("Visa Platinum 7000792289606361")
    'Visa Platinum XXXX XXXX XXXX 6361'

       Примеры использования:
       >>> mask_account_card("Visa Platinum 7000792289606361")
       'Visa Platinum XXXX XXXX XXXX 6361'
    >>> mask_account_card("Maestro 7000792289606361")
    'Maestro XXXX XXXX XXXX 6361'

       >>> mask_account_card("Maestro 7000792289606361")
       'Maestro XXXX XXXX XXXX 6361'
    >>> mask_account_card("Счет 73654108430135874305")
    'Счет XXXX XXXX XXXX 3015'

       >>> mask_account_card("Счет 73654108430135874305")
       'Счет XXXX XXXX XXXX 3015'
    Исключения:
    ValueError: если входная строка имеет неверный формат
    """

    list_card = card.split()
    number_card = list_card[-1]
    str_card = list_card[0:-1]


# Исправлено условие для проверки счета
    if str_card and str_card[0] and str_card.startswith("Счет"):
        result = get_mask_account(number_card)
    else:
        result = get_mask_card_number(str(number_card))
        # Ошибка 3: number_card уже строка, не нужно оборачивать в str()
        result = get_mask_card_number(number_card)

    return " ".join(str_card) + " " + result


def validate_and_mask_card(card_input: str) -> str:
def validate_card_input(card_input: str) -> None:
    """
    Валидация входной строки карты/счета.

    Ошибка 4: Функция должна возвращать None и правильно называться
    """
    if not card_input or not any(c.isdigit() for c in card_input):
        raise ValueError("Invalid card format: no digits found")

    # Дополнительная проверка: должно быть минимум 2 части (тип и номер)
    parts = card_input.split()
    if len(parts) < 2:
        raise ValueError("Invalid card format: missing card type or number")


def get_date(date_string: str) -> str:
    """
        >>> get_date("2024-03-11T02:26:18.671407")
        '11.03.2024'
    """
    # Парсинг строки даты в объект datetime (автоматически обрабатывает ISO-формат)
    dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
    try:
        # Парсинг строки даты в объект datetime (автоматически обрабатывает ISO-формат)
        dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))

        # Форматируем дату в нужный вид (DD.MM.YYYY)
        formatted_date = dt.strftime('%d.%m.%Y')

    # Форматируем дату в нужный вид (DD.MM.YYYY)
    formatted_date = dt.strftime('%d.%m.%Y')
        return formatted_date
    except ValueError as e:
        raise ValueError(f"Invalid date format: {date_string}") from e

    return formatted_date

if __name__ == "__main__":
    print("Результаты маскировки:")
    for card in card_examples:
        print(f"  {card} -> {mask_account_card(card)}")

for card in card_examples:
    print(mask_account_card(card))
    print("\nПример форматирования даты:")
    date_result = get_date("2024-03-11T02:26:18.671407")
    print(f"  2024-03-11T02:26:18.671407 -> {date_result}")