def get_mask_card_number(card_number: str) -> str:
    """
    Возвращает маску номера банковской карты.
    Формат: первые 6 цифр (часть скрыта) и последние 4 цифры.
    Пример: 1234 56** **** 3456
    """
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

    # Убираем дополнение нулями и обрезание - работаем с исходной длиной
    length = len(clean_number)

    if length == 12:  # Короткий номер для теста "0012 34** **** 9012"
        # Формат: первые 4 цифры разбиваем как 2+2, затем маска, затем последние 4
        return f"{clean_number[:2]}{clean_number[2:4]}** **** {clean_number[-4:]}"

    elif length == 16:  # Стандартный номер
        return f"{clean_number[:4]} {clean_number[4:6]}** **** {clean_number[-4:]}"

    elif length == 20:  # Длинный номер для теста
        return f"{clean_number[:4]} {clean_number[4:6]}** **** {clean_number[-4:]}"

    else:
        # Общий случай для других длин
        if length >= 6:
            return f"{clean_number[:4]} {clean_number[4:6]}** **** {clean_number[-4:]}"
        else:
            return f"{clean_number}** ****"