from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(input_string: str, card_number: str) -> str:
    """
    Маскирует номер карты или счета в зависимости от типа.

    Args:
        card_number:
        input_string (str): Строка с типом и номером карты/счета
            Примеры: "Visa Platinum 7000792289606361",
                     "Maestro 7000792289606361",
                     "Счет 73654108430135874305"

    Returns:
        str: Строка с замаскированным номером
    """
    parts = input_string.rsplit(' ', 1)
    if len(parts) != 2:
        raise ValueError("Неверный формат входной строки")

    card_type, number = parts

    if card_type == "Счет":
        return f"{card_type} {get_mask_account(number)}"
    else:
        return f"{card_type} {get_mask_card_number(card_number)}"


def get_date(date_string: str) -> str:
    """
    Преобразует строку с датой в формат ДД.ММ.ГГГГ.

    Args:
        date_string (str): Строка с датой в формате "ГГГГ-ММ-ДДТЧЧ:ММ:СС."

    Returns:
        str: Дата в формате "ДД.ММ.ГГГГ"
    """
    try:
        dt = datetime.fromisoformat(date_string.replace('T', ' '))
        return dt.strftime('%d.%m.%Y')
    except ValueError:
        raise ValueError("Неверный формат даты")
