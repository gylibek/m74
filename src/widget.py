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

       Функция принимает строку с типом карты/счета и номером,
       разделенными пробелом, и возвращает строку с замаскированным номером.
       Для карт и счетов используются разные типы маскировки.

       Параметры:
       input_string (str): входная строка с типом и номером карты/счета
           Допустимые форматы:
           - "Visa Platinum 7000792289606361"
           - "Maestro 7000792289606361"
           - "Счет 73654108430135874305"

       Возвращает:
       str: строка с замаскированным номером карты/счета

       Примеры использования:
       >>> mask_account_card("Visa Platinum 7000792289606361")
       'Visa Platinum XXXX XXXX XXXX 6361'

       >>> mask_account_card("Maestro 7000792289606361")
       'Maestro XXXX XXXX XXXX 6361'

       >>> mask_account_card("Счет 73654108430135874305")
       'Счет XXXX XXXX XXXX 3015'

       Исключения:
       ValueError: если входная строка имеет неверный формат
       """
    list_card = card.split()
    number_card = list_card[-1]
    str_card = list_card[0:-1]
    if card.startswith("Счет"):
        result = get_mask_account(number_card)
    else:
        result = get_mask_card_number(str(number_card))
    return " ".join(str_card) + " " + result


def get_date(date_string: str) -> str:
    """
    Преобразует строку с датой из технического формата в читаемый (DD.MM.YYYY).

    Параметры:
        date_string (str): Дата в формате ISO (например, "2024-03-11T02:26:18.671407")

    Возвращает:
        str: Дата в формате DD.MM.YYYY (например, "11.03.2024")

    Примеры:
        >>> get_date("2024-03-11T02:26:18.671407")
        '11.03.2024'
    """
    # Парсинг строки даты в объект datetime (автоматически обрабатывает ISO-формат)
    dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))

    # Форматируем дату в нужный вид (DD.MM.YYYY)
    formatted_date = dt.strftime('%d.%m.%Y')

    return formatted_date


for card in card_examples:
    print(mask_account_card(card))
