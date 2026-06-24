# src/widget.py
from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_info: str) -> str:
    """
    Маскирует номер карты или счета

    Args:
        card_info: Строка с типом и номером

    Returns:
        Замаскированная строка

    Raises:
        ValueError: Если формат входной строки некорректный
    """
    # Проверяем на пустую строку или только пробелы
    if not card_info or not card_info.strip():
        raise ValueError("Invalid card format")

    # Разбиваем строку на части
    parts = card_info.split()

    # Проверяем, что есть хотя бы тип и номер
    if len(parts) < 2:
        raise ValueError("Invalid card format")

    # Проверяем, что последняя часть - это номер (состоит только из цифр)
    number = parts[-1]
    if not number.isdigit():
        raise ValueError("Invalid card format")

    # Определяем тип карты/счета (все части кроме последней)
    card_type = " ".join(parts[:-1])

    # Если номер длинный (20 цифр) или начинается со счета - это счет
    if len(number) == 20 or "Счет" in card_type:
        return f"{card_type} {get_mask_account(number)}"
    else:
        return f"{card_type} {get_mask_card_number(number)}"
