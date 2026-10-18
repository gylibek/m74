"""Тесты для функций из модуля src.processing."""

from src.processing import process_bank_operations, process_bank_search


def test_process_bank_search_finds_by_substring() -> None:
    """Поиск находит все транзакции по подстроке."""
    data = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод с карты на карту"},
    ]
    result = process_bank_search(data, "Перевод")
    assert len(result) == 2


def test_process_bank_search_case_insensitive() -> None:
    """Поиск не зависит от регистра."""
    data = [{"description": "перевод организации"}]
    assert len(process_bank_search(data, "ПЕРЕВОД")) == 1


def test_process_bank_search_uses_regex() -> None:
    """Функция работает как регулярное выражение."""
    data = [
        {"description": "Payment #123"},
        {"description": "Payment"},
        {"description": "Other"},
    ]
    result = process_bank_search(data, r"Payment #\d+")
    assert len(result) == 1
    assert result[0]["description"] == "Payment #123"


def test_process_bank_search_no_matches() -> None:
    """Пустой результат, если ничего не найдено."""
    assert process_bank_search([{"description": "x"}], "нет") == []


def test_process_bank_search_empty_input() -> None:
    """Пустой список на входе — пустой список на выходе."""
    assert process_bank_search([], "test") == []


def test_process_bank_search_skips_missing_description() -> None:
    """Транзакции без поля description не падают и не находятся."""
    data = [{"id": 1}, {"description": "test"}]
    assert len(process_bank_search(data, "test")) == 1


def test_process_bank_operations_counts_correctly() -> None:
    """Считает количество по каждой категории."""
    data = [
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
    ]
    result = process_bank_operations(
        data, ["Перевод организации", "Открытие вклада"]
    )
    assert result == {"Перевод организации": 2, "Открытие вклада": 1}


def test_process_bank_operations_ignores_unknown_categories() -> None:
    """Категории, которых нет в data, в результат не попадают."""
    data = [{"description": "Перевод"}, {"description": "Другое"}]
    assert process_bank_operations(data, ["Перевод"]) == {"Перевод": 1}


def test_process_bank_operations_empty() -> None:
    """Пустой список на входе — пустой словарь."""
    assert process_bank_operations([], ["test"]) == {}


def test_process_bank_operations_no_matches() -> None:
    """Если ни одна категория не встретилась — пустой словарь."""
    data = [{"description": "Другое"}]
    assert process_bank_operations(data, ["Нет такого"]) == {}
