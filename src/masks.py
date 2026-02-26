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
    masked = f"{card_str[:4]} {card_str[4:6]}** ****"
    masked += f" {card_str[-4:]}"
    return masked


def get_mask_account(account_number: str) -> str:
    """
    Возвращает маску номера банковского счета в формате **XXXX

    Args:
        account_number (int): номер счета

    Returns:
        str: замаскированный номер счета
    """
    # Преобразуем число в строку и берем последние 4 цифры
    masked = f"**{account_number[-4:]}"
    return masked
