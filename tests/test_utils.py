# tests/test_utils.py
import json
from unittest.mock import mock_open, patch
from src.utils import get_transactions


def test_get_transactions_success() -> None:
    """Успешное чтение корректного JSON-списка."""
    mock_data = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
    m = mock_open(read_data=json.dumps(mock_data))
    with patch("builtins.open", m):
        result = get_transactions("dummy_path")
    assert result == mock_data


def test_get_transactions_empty_file() -> None:
    """Пустой файл -> пустой список."""
    m = mock_open(read_data="")
    with patch("builtins.open", m):
        result = get_transactions("dummy_path")
    assert result == []


def test_get_transactions_not_list() -> None:
    """Файл содержит не список -> пустой список."""
    m = mock_open(read_data='{"key": "value"}')
    with patch("builtins.open", m):
        result = get_transactions("dummy_path")
    assert result == []


def test_get_transactions_file_not_found() -> None:
    """Файл не найден -> пустой список."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = get_transactions("missing.json")
    assert result == []


def test_get_transactions_invalid_json() -> None:
    """Некорректный JSON -> пустой список."""
    m = mock_open(read_data="not a json")
    with patch("builtins.open", m):
        result = get_transactions("dummy_path")
    assert result == []
