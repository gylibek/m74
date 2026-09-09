import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/convert"


def convert_currency(transaction: Dict[str, Any]) -> float:
    amount = transaction.get("amount")
    if amount is None:
        return 0.0

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
        result = data.get("result")
        return float(result) if result is not None else float(amount)
    except Exception:  # перехватываем все исключения
        return float(amount)
