# src/utils.py
import json
import logging
import os
from typing import Any, Dict, List

# ----- Логгер для utils -----
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

os.makedirs("logs", exist_ok=True)  # создаём папку, если нет

file_handler = logging.FileHandler(
    "logs/utils.log",
    mode="w",
    encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def get_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список транзакций.
    В случае ошибки возвращает пустой список.
    """
    logger.info(f"Attempting to read transactions from {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            logger.info(f"Successfully loaded {len(data)} transactions")
            return data
        else:
            logger.warning("Data is not a list, returning []")
            return []
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return []
