from typing import Iterator, List, Dict, Any


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданной валюте.

    Args:
        transactions: Список словарей с транзакциями
        currency_code: Код валюты для фильтрации (например, "USD")

    Returns:
        Итератор, выдающий транзакции с указанной валютой

    Example:
        >>> transactions = [
        ...     {"operationAmount": {"currency": {"code": "USD"}}, "description": "Payment 1"},
        ...     {"operationAmount": {"currency": {"code": "EUR"}}, "description": "Payment 2"}
        ... ]
        >>> usd_transactions = filter_by_currency(transactions, "USD")
        >>> next(usd_transactions)["description"]
        'Payment 1'
    """
    for transaction in transactions:
        try:
            if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency_code:
                yield transaction
        except (AttributeError, TypeError):
            continue


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генератор описаний транзакций.

    Args:
        transactions: Список словарей с транзакциями

    Returns:
        Итератор с описаниями каждой транзакции

    Example:
        >>> transactions = [
        ...     {"description": "Перевод организации"},
        ...     {"description": "Перевод со счета на счет"}
        ... ]
        >>> descriptions = transaction_descriptions(transactions)
        >>> next(descriptions)
        'Перевод организации'
    """
    for transaction in transactions:
        try:
            yield transaction.get("description", "")
        except (AttributeError, TypeError):
            yield ""


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

    Args:
        start: Начальное значение диапазона (включительно)
        stop: Конечное значение диапазона (включительно)

    Returns:
        Итератор с номерами карт в формате XXXX XXXX XXXX XXXX

    Example:
        >>> for card_number in card_number_generator(1, 3):
        ...     print(card_number)
        0000 0000 0000 0001
        0000 0000 0000 0002
        0000 0000 0000 0003

    Raises:
        ValueError: Если start или stop выходят за допустимый диапазон [1, 9999999999999999]
    """
    if not (1 <= start <= 9999999999999999 and 1 <= stop <= 9999999999999999):
        raise ValueError("Номера карт должны быть в диапазоне от 1 до 9999999999999999")

    if start > stop:
        raise ValueError("Начальное значение не может быть больше конечного")

    for number in range(start, stop + 1):
        formatted = f"{number:016d}"
        yield f"{formatted[:4]} {formatted[4:8]} {formatted[8:12]} {formatted[12:16]}"
