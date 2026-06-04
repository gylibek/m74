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
    card (str): входная строка с типом и номером карты/счета
        Допустимые форматы:
        - "Visa Platinum 7000792289606361"
        - "Maestro 7000792289606361"
        - "Счет 73654108430135874305"

    Возвращает:
    str: строка с замаскированным номером карты/счета

    Примеры использования:
    >>> mask_account_card("Visa Platinum 7000792289606361")
    'Visa Platinum 7000 79** **** 6361'
    >>> mask_account_card("Maestro 7000792289606361")
    'Maestro 7000 79** **** 6361'
    >>> mask_account_card("Счет 73654108430135874305")
    'Счет **4305'
    """
    # Разделяем строку на части
    parts = card.split()

    # Последняя часть - это номер
    number_card = parts[-1]
    # Все остальные части - это название карты/счета
    card_name_parts = parts[:-1]
    card_name = " ".join(card_name_parts)

    # Проверяем, является ли это счетом
    if card_name == "Счет":
        result = get_mask_account(number_card)
    else:
        result = get_mask_card_number(number_card)

    return f"{card_name} {result}"


def validate_card_input(card_input: str) -> None:
    """
    Валидация входной строки карты/счета.
    """
    if not card_input or not any(c.isdigit() for c in card_input):
        raise ValueError("Invalid card format: no digits found")

    # Дополнительная проверка: должно быть минимум 2 части (тип и номер)
    parts = card_input.split()
    if len(parts) < 2:
        raise ValueError("Invalid card format: missing card type or number")


def get_date(date_string: str) -> str:
    """
    Преобразует строку даты в формат DD.MM.YYYY

    >>> get_date("2024-03-11T02:26:18.671407")
    '11.03.2024'
    """
    try:
        # Парсинг строки даты в объект datetime (автоматически обрабатывает ISO-формат)
        dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))

        # Форматируем дату в нужный вид (DD.MM.YYYY)
        formatted_date = dt.strftime('%d.%m.%Y')
        return formatted_date
    except ValueError as e:
        raise ValueError(f"Invalid date format: {date_string}") from e


if __name__ == "__main__":
    print("Результаты маскировки:")
    for card in card_examples:
        print(f"  {card} -> {mask_account_card(card)}")

    print("\nПример форматирования даты:")
    date_result = get_date("2024-03-11T02:26:18.671407")
    print(f"  2024-03-11T02:26:18.671407 -> {date_result}")
