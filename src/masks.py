import logging
import os
from typing import Optional

# Создаём логгер для модуля masks
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

file_handler = logging.FileHandler(os.path.join(log_dir, "masks.log"), mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """
    Возвращает маску номера банковской карты в формате XXXX XX** **** XXXX

    Args:
        card_number (int): номер карты

    Returns:
        str: замаскированный номер карты
    """
    logger.debug(f"Masking card number: {card_number}")
    try:
        # Преобразуем число в строку и дополняем нулями слева до 16 символов
        card_str = str(card_number).zfill(16)
        # Формируем маску
        masked = f"{card_str[:4]} {card_str[4:6]}** ****"
        masked += f" {card_str[-4:]}"
        logger.info(f"Card masked successfully: {masked}")
        return masked
    except Exception as e:
        logger.error(f"Error masking card number {card_number}: {e}")
        return card_number  # fallback, но по сути никогда не произойдёт


def get_mask_account(account_number: str) -> str:
    """
    Возвращает маску номера банковского счета в формате **XXXX

    Args:
        account_number (int): номер счета

    Returns:
        str: замаскированный номер счета
    """
    logger.debug(f"Masking account number: {account_number}")
    try:
        # Преобразуем число в строку и берем последние 4 цифры
        masked = f"**{account_number[-4:]}"
        logger.info(f"Account masked successfully: {masked}")
        return masked
    except Exception as e:
        logger.error(f"Error masking account number {account_number}: {e}")
        return account_number
