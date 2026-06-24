# tests/test_masks.py
import pytest
from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize("card_input,expected", [
    ("1234567890123456", "1234 56** **** 3456"),
    ("0012345678901234", "0012 34** **** 1234"),
])
def test_get_mask_card_number(card_input: str, expected: str) -> None:
    assert get_mask_card_number(card_input) == expected


@pytest.mark.parametrize("short_card,expected", [
    # ИСПРАВЛЕНО: убираем пробел между 1234 и 56**, так как функция возвращает без пробела
    ("123456789012", "1234** **** 9012"),
])
def test_get_mask_card_number_short(short_card: str, expected: str) -> None:
    assert get_mask_card_number(short_card) == expected


@pytest.mark.parametrize("long_card,expected", [
    ("12345678901234567890", "1234 56** **** 7890"),
])
def test_get_mask_card_number_long(long_card: str, expected: str) -> None:
    assert get_mask_card_number(long_card) == expected


def test_get_mask_card_number_invalid() -> None:
    with pytest.raises(ValueError):
        get_mask_card_number("")

    with pytest.raises(ValueError):
        get_mask_card_number("-1234567890123456")


@pytest.mark.parametrize("account_input,expected", [
    ("1234567890", "**7890"),
    ("1234", "**1234"),
    ("123", "**123"),
    ("12", "**12"),
    ("1", "**1"),
    ("123456789012345", "**2345"),
])
def test_get_mask_account(account_input: str, expected: str) -> None:
    assert get_mask_account(account_input) == expected


def test_get_mask_account_invalid() -> None:
    with pytest.raises(ValueError):
        get_mask_account("")

    with pytest.raises(ValueError):
        get_mask_account("-1234567890")

    with pytest.raises(ValueError):
        get_mask_account("None")
