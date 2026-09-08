# tests/test_external_api.py
import pytest
from unittest.mock import patch
from src.external_api import convert_currency


@patch("src.external_api.requests.get")
def test_convert_currency_usd(mock_get) -> None:
    """Конвертация USD в рубли."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 7500.0}

    transaction = {"amount": 100, "currency": "USD"}
    result = convert_currency(transaction)
    assert result == 7500.0
    mock_get.assert_called_once()


@patch("src.external_api.requests.get")
def test_convert_currency_eur(mock_get) -> None:
    """Конвертация EUR в рубли."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 9000.0}

    transaction = {"amount": 100, "currency": "EUR"}
    result = convert_currency(transaction)
    assert result == 9000.0


def test_convert_currency_rub() -> None:
    """Если валюта RUB, конвертация не требуется."""
    transaction = {"amount": 100, "currency": "RUB"}
    result = convert_currency(transaction)
    assert result == 100.0


@patch("src.external_api.requests.get")
def test_convert_currency_api_error(mock_get) -> None:
    """При ошибке API возвращается исходная сумма."""
    mock_get.side_effect = Exception("API error")
    transaction = {"amount": 100, "currency": "USD"}
    result = convert_currency(transaction)
    assert result == 100.0  # возвращаем исходную сумму
