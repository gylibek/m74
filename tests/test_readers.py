"""Тесты для модуля чтения финансовых операций из файлов."""

import json
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
import pytest

from src.readers import (
    read_transactions_csv,
    read_transactions_excel,
    read_transactions_json,
)

# ---------------------------------------------------------------------------
# JSON
# ---------------------------------------------------------------------------


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data=json.dumps(
        [
            {"id": 1, "amount": 100, "description": "Перевод"},
            {"id": 2, "amount": 200, "description": "Вклад"},
        ]
    ),
)
def test_read_transactions_json_returns_list_of_dicts(
    mock_file: MagicMock,
) -> None:
    """JSON-ридер возвращает список словарей с транзакциями."""
    result = read_transactions_json("fake.json")

    assert result == [
        {"id": 1, "amount": 100, "description": "Перевод"},
        {"id": 2, "amount": 200, "description": "Вклад"},
    ]
    mock_file.assert_called_once_with("fake.json", encoding="utf-8")


@patch("builtins.open", new_callable=mock_open, read_data="[]")
def test_read_transactions_json_empty_file(mock_file: MagicMock) -> None:
    """Пустой JSON-массив даёт пустой список."""
    assert read_transactions_json("empty.json") == []
    mock_file.assert_called_once_with("empty.json", encoding="utf-8")


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data='[{"id": 1}, {"id": 2}]',
)
def test_read_transactions_json_does_not_raise(
    mock_file: MagicMock,
) -> None:
    """JSON-ридер не падает и не теряет элементы."""
    result = read_transactions_json("data.json")
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(item, dict) for item in result)


# ---------------------------------------------------------------------------
# CSV
# ---------------------------------------------------------------------------


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data="id,amount,category\n1,100,food\n2,200,transport\n",
)
def test_read_transactions_csv_returns_list_of_dicts(
    mock_file: MagicMock,
) -> None:
    """CSV-ридер возвращает список словарей с транзакциями."""
    result = read_transactions_csv("fake.csv")

    assert result == [
        {"id": "1", "amount": "100", "category": "food"},
        {"id": "2", "amount": "200", "category": "transport"},
    ]
    mock_file.assert_called_once_with("fake.csv", encoding="utf-8")


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data="id,amount,category\n",
)
def test_read_transactions_csv_only_header(mock_file: MagicMock) -> None:
    """CSV-файл только с заголовком даёт пустой список."""
    assert read_transactions_csv("empty.csv") == []
    mock_file.assert_called_once_with("empty.csv", encoding="utf-8")


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data="id,amount,category\n1,100,food\n",
)
def test_read_transactions_csv_returns_plain_dicts(
    mock_file: MagicMock,
) -> None:
    """Каждый элемент результата — обычный dict."""
    result = read_transactions_csv("one.csv")
    assert type(result[0]) is dict
    assert result[0] == {"id": "1", "amount": "100", "category": "food"}


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data="id,amount\n1,100\n2,200\n3,300\n",
)
def test_read_transactions_csv_multiple_rows(
    mock_file: MagicMock,
) -> None:
    """CSV-ридер корректно обрабатывает несколько строк."""
    result = read_transactions_csv("many.csv")
    assert len(result) == 3
    assert [row["id"] for row in result] == ["1", "2", "3"]


@patch("builtins.open", side_effect=FileNotFoundError)
def test_read_transactions_csv_file_not_found(
    mock_file: MagicMock,
) -> None:
    """Если файла нет — пробрасывается FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        read_transactions_csv("missing.csv")


# ---------------------------------------------------------------------------
# Excel
# ---------------------------------------------------------------------------


@patch("src.readers.pd.read_excel")
def test_read_transactions_excel_returns_list_of_dicts(
    mock_read_excel: MagicMock,
) -> None:
    """Excel-ридер возвращает список словарей с транзакциями."""
    mock_read_excel.return_value = pd.DataFrame(
        [
            {"id": 1, "amount": 100, "category": "food"},
            {"id": 2, "amount": 200, "category": "transport"},
        ]
    )

    result = read_transactions_excel("fake.xlsx")

    assert result == [
        {"id": 1, "amount": 100, "category": "food"},
        {"id": 2, "amount": 200, "category": "transport"},
    ]
    mock_read_excel.assert_called_once_with("fake.xlsx")


@patch("src.readers.pd.read_excel")
def test_read_transactions_excel_empty_dataframe(
    mock_read_excel: MagicMock,
) -> None:
    """Пустой DataFrame даёт пустой список."""
    mock_read_excel.return_value = pd.DataFrame()

    assert read_transactions_excel("empty.xlsx") == []
    mock_read_excel.assert_called_once_with("empty.xlsx")


@patch("src.readers.pd.read_excel")
def test_read_transactions_excel_stringifies_keys(
    mock_read_excel: MagicMock,
) -> None:
    """Ключи каждой записи приводятся к строке."""
    mock_read_excel.return_value = pd.DataFrame({0: ["a"], 1: ["b"]})

    result = read_transactions_excel("numeric_cols.xlsx")

    assert result == [{"0": "a", "1": "b"}]
    assert all(isinstance(key, str) for key in result[0])


@patch("src.readers.pd.read_excel")
def test_read_transactions_excel_passes_path_as_is(
    mock_read_excel: MagicMock,
) -> None:
    """Путь передаётся в pandas без изменений."""
    mock_read_excel.return_value = pd.DataFrame([{"id": 1}])
    read_transactions_excel("nested/dir/file.xlsx")
    mock_read_excel.assert_called_once_with("nested/dir/file.xlsx")


@patch("src.readers.pd.read_excel", side_effect=FileNotFoundError)
def test_read_transactions_excel_file_not_found(
    mock_read_excel: MagicMock,
) -> None:
    """Если файла нет — pandas кидает FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        read_transactions_excel("missing.xlsx")
