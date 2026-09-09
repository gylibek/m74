# src/utils.py
import json
import logging
import os
from typing import Any, Dict, List

# Создаём логгер для модуля utils
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

# Создаём папку logs, если её нет
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Настраиваем file_handler (перезапись при каждом запуске)
file_handler = logging.FileHandler(os.path.join(log_dir, "utils.log"), mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Формат: время, имя модуля, уровень, сообщение
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def get_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл с транзакциями и возвращает список словарей.

    Аргументы:
        file_path (str): путь к файлу JSON.

    Возвращает:
        List[Dict[str, Any]]: список транзакций. Если файл пуст, повреждён,
        не является списком или не найден, возвращает пустой список.
    """
    logger.info(f"Attempting to read transactions from {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            logger.info(f"Successfully loaded {len(data)} transactions from {file_path}")
            return data
        else:
            logger.warning(f"Data in {file_path} is not a list, returning empty list")
            return []
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_path}: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error while reading {file_path}: {e}")
        return []
