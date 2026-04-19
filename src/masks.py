def get_mask_card_number(card_number: str) -> str:
    """
    Возвращает маску номера банковской карты в формате XXXX XX** **** XXXX

    Args:
        card_number (int): номер карты

    Returns:
        str: замаскированный номер карты
    """
    # Преобразуем число в строку и дополняем нулями слева до 16 символов
    card_str = str(card_number).zfill(16)
    # Формируем маску
    masked = f"{card_str[:3]} {card_str[3:6]}** ****"
    masked += f" {card_str[-3:]}"
    return masked


def get_mask_account(account_number: str) -> str:
    """
    Возвращает маску номера банковского счета в формате **XXXX

    Args:
        account_number (int): номер счета

    Returns:
        str: замаскированный номер счета
    """
    # Преобразуем число в строку и берем последние 3 цифры
    masked = f"**{account_number[-3:]}"
    return masked
