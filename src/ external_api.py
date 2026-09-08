# src/external_api.py
import os
import requests
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()  # загружаем переменные из .env

API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/convert"


def convert_currency(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли, если валюта USD или EUR.

    Аргументы:
        transaction (Dict[str, Any]): словарь с ключами 'amount' и 'currency'.

    Возвращает:
        float: сумма в рублях. Если валюта не USD/EUR, возвращает исходную сумму.
    """
    amount = transaction.get("amount")
    currency = transaction.get("currency", "RUB").upper()

    if currency not in ("USD", "EUR"):
        return float(amount)

    if not API_KEY:
        raise ValueError("API key for exchange rates is not set")

    params = {
        "from": currency,
        "to": "RUB",
        "amount": amount,
    }
    headers = {"apikey": API_KEY}

    try:
        response = requests.get(BASE_URL, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        return float(data.get("result", amount))
    except (requests.RequestException, KeyError, ValueError):
        # В случае ошибки возвращаем исходную сумму
        return float(amount)
