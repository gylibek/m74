# src/masks.py
import logging
import os

# ----- Логгер для masks -----
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

os.makedirs("logs", exist_ok=True)

file_handler = logging.FileHandler(
    "logs/masks.log",
    mode="w",
    encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты: XXXX XX** **** XXXX
    """
    logger.debug(f"Masking card number: {card_number}")
    try:
        card_str = str(card_number).zfill(16)
        masked = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"
        logger.info(f"Card masked successfully: {masked}")
        return masked
    except Exception as e:
        logger.error(f"Error masking card {card_number}: {e}")
        return str(card_number)  # fallback


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счета: **XXXX
    """
    logger.debug(f"Masking account number: {account_number}")
    try:
        masked = f"**{account_number[-4:]}"
        logger.info(f"Account masked successfully: {masked}")
        return masked
    except Exception as e:
        logger.error(f"Error masking account {account_number}: {e}")
        return str(account_number)
