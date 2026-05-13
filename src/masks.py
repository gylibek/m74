def get_mask_card_number(card_number: str) -> str:
    """
    Возвращает маску номера банковской карты.
    Формат: первые 6 цифр (часть скрыта) и последние 4 цифры.
    Пример: 1234 56XX XXXX 3456
    """
    # Проверка на валидность
    if not isinstance(card_number, str):
        raise TypeError("Номер карты должен быть строкой")

    if not card_number:
        raise ValueError("Номер карты не может быть пустым")

    if card_number.startswith('-'):
        raise ValueError("Номер карты не может быть отрицательным")

    # Очищаем от лишних пробелов
    clean_number = card_number.replace(" ", "")

    # Проверяем, что все символы - цифры
    if not clean_number.isdigit():
        raise ValueError("Номер карты должен состоять только из цифр")

    # Для коротких номеров дополняем нулями слева
    if len(clean_number) < 16:
        clean_number = clean_number.zfill(16)

    # Для длинных номеров берем последние 16 цифр
    if len(clean_number) > 16:
        clean_number = clean_number[-16:]

    # Логика маски: первые 6 цифр, последние 4 цифры
    first_six = clean_number[:6]
    last_four = clean_number[-4:]

    # Форматируем: XXXX XX** **** XXXX
    # 1234 56XX XXXX 3456
    return f"{first_six[:4]} {first_six[4:6]}XX XXXX {last_four}"


def get_mask_account(account_number: str) -> str:
    """
    Возвращает маску номера банковского счета.
    Формат: две звездочки и последние 4 цифры (или меньше, если счет короче).
    Пример: **7890
    """
    if not isinstance(account_number, str):
        raise TypeError("Номер счета должен быть строкой")

    if not account_number:
        raise ValueError("Номер счета не может быть пустым")

    if account_number.startswith('-'):
        raise ValueError("Номер счета не может быть отрицательным")

    # Очищаем от лишних пробелов
    clean_number = account_number.replace(" ", "")

    # Проверяем, что все символы - цифры
    if not clean_number.isdigit():
        raise ValueError("Номер счета должен состоять только из цифр")

    # Берем последние 4 цифры (или меньше, если номер короче)
    if len(clean_number) >= 4:
        last_digits = clean_number[-4:]
    else:
        last_digits = clean_number

    return f"**{last_digits}"