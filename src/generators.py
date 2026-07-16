"""
Модуль generators.py

Содержит три функции-генератора для работы с банковскими транзакциями:
1. filter_by_currency – фильтрует транзакции по коду валюты.
2. transaction_descriptions – извлекает описания транзакций.
3. card_number_generator – генерирует номера карт в заданном диапазоне.

Все функции возвращают итераторы (используют yield), что позволяет
экономить память при работе с большими объёмами данных.
"""

from typing import Iterator, Dict, Any, Generator


# ======================================================================
# 1. Функция-фильтр по валюте
# ======================================================================
def filter_by_currency(transactions: list[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    Генератор, который выдаёт только те транзакции, у которых код валюты
    совпадает с заданным.

    Параметры:
        transactions (list[dict]) – список словарей с данными о транзакциях.
        currency_code (str) – код валюты для фильтрации (например, 'USD').

    Возвращает:
        Iterator[dict] – итератор, поочерёдно выдающий подходящие транзакции.

    Пример:
        >>> transactions = [{"operationAmount": {"currency": {"code": "USD"}}}, ...]
        >>> usd = filter_by_currency(transactions, "USD")
        >>> for t in usd:
        ...     print(t)
    """
    for transaction in transactions:
        # Безопасно пытаемся получить код валюты
        try:
            # Обращаемся по цепочке ключей operationAmount -> currency -> code
            op_amount = transaction.get("operationAmount", {})
            currency = op_amount.get("currency", {})
            code = currency.get("code")
            # Если код совпадает с искомым – возвращаем транзакцию
            if code == currency_code:
                yield transaction
        except (AttributeError, TypeError):
            # Если структура транзакции не соответствует ожидаемой,
            # просто пропускаем её (не прерываем работу генератора)
            continue


# ======================================================================
# 2. Генератор описаний транзакций
# ======================================================================
def transaction_descriptions(transactions: list[Dict[str, Any]]) -> Generator[str, None, None]:
    """
    Генератор, который возвращает описание каждой транзакции из списка.

    Параметры:
        transactions (list[dict]) – список словарей с транзакциями.

    Возвращает:
        Generator[str] – генератор строк с описанием. Если описание отсутствует,
                         выдаётся строка "Описание отсутствует".

    Пример:
        >>> transactions = [{"description": "Оплата"}, {"description": None}]
        >>> for desc in transaction_descriptions(transactions):
        ...     print(desc)
        Оплата
        Описание отсутствует
    """
    for transaction in transactions:
        # Извлекаем значение по ключу "description"
        description = transaction.get("description")
        # Если ключа нет или значение равно None – подставляем заглушку
        if description is None:
            description = "Описание отсутствует"
        yield description


# ======================================================================
# 3. Генератор номеров банковских карт
# ======================================================================
def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """
    Генератор номеров банковских карт в заданном диапазоне.

    Параметры:
        start (int) – начальное число диапазона (включительно).
        stop (int) – конечное число диапазона (включительно).

    Возвращает:
        Generator[str] – генератор строк с номерами карт в формате
                         "XXXX XXXX XXXX XXXX". Каждый номер состоит из 16 цифр,
                         дополненных ведущими нулями при необходимости.

    Пример:
        >>> for card in card_number_generator(1, 3):
        ...     print(card)
        0000 0000 0000 0001
        0000 0000 0000 0002
        0000 0000 0000 0003
    """
    for number in range(start, stop + 1):
        # Форматируем число как 16-значную строку с ведущими нулями
        card_str = f"{number:016d}"
        # Разбиваем на группы по 4 цифры и соединяем пробелами
        formatted = f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:]}"
        yield formatted


# ======================================================================
# Небольшой тест при запуске файла как самостоятельного скрипта
# ======================================================================
if __name__ == "__main__":
    # Пример использования (можно удалить или закомментировать)
    sample_transactions = [
        {
            "id": 1,
            "description": "Перевод другу",
            "operationAmount": {"amount": "150.00", "currency": {"code": "USD"}}
        },
        {
            "id": 2,
            "description": "Покупка в магазине",
            "operationAmount": {"amount": "75.50", "currency": {"code": "EUR"}}
        },
        {
            "id": 3,
            "description": "Пополнение счета",
            "operationAmount": {"amount": "1000.00", "currency": {"code": "RUB"}}
        }
    ]

    print("=== filter_by_currency (USD) ===")
    for t in filter_by_currency(sample_transactions, "USD"):
        print(f"ID {t['id']}: {t['description']}")

    print("\n=== transaction_descriptions ===")
    for desc in transaction_descriptions(sample_transactions):
        print(desc)

    print("\n=== card_number_generator (от 1 до 5) ===")
    for card in card_number_generator(1, 5):
        print(card)