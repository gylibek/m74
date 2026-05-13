import pytest

# Импортируем модуль
from src.masks import get_mask_account, get_mask_card_number


# Тесты для функции get_mask_card_number
@pytest.mark.parametrize("card_input,expected", [
    ("1234567890123456", "1234 56XX XXXX 3456"),
    ("0012345678901234", "0012 34XX XXXX 1234"),
    ("1234567890123456", "1234 56XX XXXX 3456"),
])
def test_get_mask_card_number(card_input: str, expected: str) -> None:
    assert get_mask_card_number(card_input) == expected


@pytest.mark.parametrize("short_card,expected", [
    ("123456789012", "0012 34XX XXXX 9012"),
    ("1", "0000 00XX XXXX 0001"),
])
def test_get_mask_card_number_short(short_card: str, expected: str) -> None:
    assert get_mask_card_number(short_card) == expected


@pytest.mark.parametrize("long_card,expected", [
    ("12345678901234567890", "5678 90XX XXXX 8900"),
])
def test_get_mask_card_number_long(long_card: str, expected: str) -> None:
    assert get_mask_card_number(long_card) == expected


def test_get_mask_card_number_invalid() -> None:
    with pytest.raises(ValueError):
        get_mask_card_number("")

    with pytest.raises(ValueError):
        get_mask_card_number("-1234567890123456")


# Тесты для функции get_mask_account
@pytest.mark.parametrize("account_input,expected", [
    ("1234567890", "**7890"),
    ("1234", "**1234"),
    ("123", "**123"),
    ("12", "**12"),
    ("1", "**1"),
    ("123456789012345", "**345"),
    ("1234567890", "**7890"),
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