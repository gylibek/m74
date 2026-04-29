def get_mask_card_number(card_number: str) -> str:
    """
    Возвращает маску номера банковской карты.
    Формат: первые 6 цифр (часть скрыта) и последние 4 цифры.
    Пример: 1234 56XX XXXX 3456
    """
    # Проверка на валидность (чтобы проходили тесты на ValueError)
    if not isinstance(card_number, str) or not card_number.isdigit():
        raise ValueError("Номер карты должен быть строкой, состоящей только из цифр")

    # Очищаем от лишних пробелов, если они есть
    clean_number = card_number.replace(" ", "")

    if len(clean_number) < 4:
        raise ValueError("Номер карты слишком короткий")

    # Логика маски: берем первые 4, затем 2, затем скрываем середину, затем последние 4
    first_part = clean_number[:4]
    second_part = clean_number[4:6]
    last_part = clean_number[-4:]

    return f"{first_part} {second_part}XX XXXX {last_part}"


def get_mask_account(account_number: str) -> str:
    """
    Возвращает маску номера банковского счета.
    Формат: скрываем начало, оставляем последние 4 цифры.
    Пример: XXXX XXXX XXXX 1234
    """
    if not isinstance(account_number, str) or not account_number.isdigit():
        raise ValueError("Номер счета должен быть строкой, состоящей только из цифр")

    clean_number = account_number.replace(" ", "")

    if len(clean_number) < 4:
        raise ValueError("Номер счета слишком короткий")

    # Берем только последние 4 цифры и добавляем маску в начале
    last_four = clean_number[-4:]
    return f"XXXX XXXX XXXX {last_four}"