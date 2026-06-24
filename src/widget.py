# src/widget.py
from datetime import datetime
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

    # Если номер длинный (20 цифр) или в типе есть "Счет" - это счет
    if len(number) == 20 or "Счет" in card_type:
        return f"{card_type} {get_mask_account(number)}"
    else:
        return f"{card_type} {get_mask_card_number(number)}"


def get_date(date_string: str) -> str:
    """
    Преобразует дату из ISO формата в формат ДД.ММ.ГГГГ

    Args:
        date_string: Строка с датой в ISO формате

    Returns:
        Строка с датой в формате ДД.ММ.ГГГГ

    Raises:
        ValueError: Если формат даты некорректный
    """
    if not date_string or not date_string.strip():
        raise ValueError("Invalid date format")

    # Очищаем строку от временной зоны и лишних символов
    clean_date = date_string.strip()

    # Удаляем Z в конце
    if clean_date.endswith('Z'):
        clean_date = clean_date[:-1]

    # Удаляем часовой пояс (+03:00, -05:00 и т.д.)
    if '+' in clean_date:
        clean_date = clean_date.split('+')[0]
    elif '-' in clean_date and clean_date.count('-') > 2:
        # Проверяем, что это часовой пояс (формат -05:00)
        parts = clean_date.rsplit('-', 1)
        if len(parts) == 2 and len(parts[1]) in [2, 5, 6]:  # -05, -05:00, -05:00:00
            clean_date = parts[0]

    # Пробуем разные форматы - сначала без микросекунд, потом с ними
    formats = [
        '%Y-%m-%dT%H:%M:%S',  # без микросекунд (ВАЖНО: сначала этот формат!)
        '%Y-%m-%dT%H:%M:%S.%f',  # с микросекундами
        '%Y-%m-%d %H:%M:%S',  # с пробелом без микросекунд
        '%Y-%m-%d %H:%M:%S.%f',  # с пробелом и микросекундами
        '%Y-%m-%d',  # только дата
    ]

    for fmt in formats:
        try:
            date_obj = datetime.strptime(clean_date, fmt)
            return date_obj.strftime('%d.%m.%Y')
        except (ValueError, TypeError):
            continue

    raise ValueError("Invalid date format")
