
import re
from collections import Counter
from typing import Any


def process_bank_search(
    data: list[dict[str, Any]], search: str
) -> list[dict[str, Any]]:
    """Ищет транзакции, в описании которых встречается заданная строка.

    Поиск выполняется с помощью библиотеки ``re`` без учёта регистра.

    Args:
        data: Список словарей с банковскими операциями.
        search: Строка (или регулярное выражение) для поиска
            в поле ``description``.

    Returns:
        Список транзакций, у которых ``description`` соответствует
        переданному шаблону.
    """
    pattern = re.compile(search, re.IGNORECASE)
    return [
        transaction
        for transaction in data
        if pattern.search(str(transaction.get("description", "")))
    ]


def process_bank_operations(
    data: list[dict[str, Any]], categories: list[str]
) -> dict[str, int]:
    """Считает количество операций по каждой из заданных категорий.

    Категория операции берётся из поля ``description``. В расчёт
    попадают только те операции, чьё описание точно совпадает
    с одной из переданных категорий.

    Args:
        data: Список словарей с банковскими операциями.
        categories: Список категорий (значений поля ``description``),
            по которым необходимо выполнить подсчёт.

    Returns:
        Словарь, где ключ — название категории,
        а значение — количество операций в этой категории.
    """
    counter: Counter[str] = Counter()
    for transaction in data:
        description = str(transaction.get("description", ""))
        if description in categories:
            counter[description] += 1
    return dict(counter)
