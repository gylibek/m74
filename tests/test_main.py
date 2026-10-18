"""Тесты для CLI-функции main из модуля src.main."""

from typing import Any

import pytest

import src.main as main_module


def _feed_inputs(
    monkeypatch: pytest.MonkeyPatch, values: list[str]
) -> None:
    """Подменяет input() последовательностью заранее заданных ответов."""
    answers = iter(values)
    monkeypatch.setattr(
        "builtins.input", lambda *args, **kwargs: next(answers)
    )


def test_main_full_flow(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Полный проход: JSON -> EXECUTED -> без сортировки/фильтров."""
    transactions: list[dict[str, Any]] = [
        {
            "state": "EXECUTED",
            "date": "2019-12-08T22:46:21.935582",
            "description": "Открытие вклада",
            "operationAmount": {
                "amount": "40542.00",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "to": "Счет 4321",
        }
    ]
    monkeypatch.setattr(
        main_module, "read_transactions_json", lambda p: transactions
    )
    _feed_inputs(monkeypatch, ["1", "EXECUTED", "нет", "нет", "нет"])

    main_module.main()
    out = capsys.readouterr().out

    assert "Всего банковских операций в выборке: 1" in out
    assert "08.12.2019 Открытие вклада" in out
    assert "Сумма: 40542.00 руб." in out


def test_main_invalid_status_retry(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Неверный статус не роняет программу, а просит повторить ввод."""
    monkeypatch.setattr(
        main_module, "read_transactions_json", lambda p: []
    )
    _feed_inputs(
        monkeypatch,
        ["1", "test", "EXECUTED", "нет", "нет", "нет"],
    )

    main_module.main()
    out = capsys.readouterr().out

    assert 'Статус операции "TEST" недоступен.' in out
    assert "Не найдено ни одной транзакции" in out


def test_main_empty_result_message(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Если выборка пуста — выводится соответствующее сообщение."""
    monkeypatch.setattr(
        main_module,
        "read_transactions_json",
        lambda p: [{"state": "CANCELED", "description": "x"}],
    )
    _feed_inputs(monkeypatch, ["1", "EXECUTED", "нет", "нет", "нет"])

    main_module.main()
    out = capsys.readouterr().out
    assert "Не найдено ни одной транзакции" in out


def test_main_only_rub_filter(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Флаг «только рублёвые» отсекает валютные операции."""
    data = [
        {
            "state": "EXECUTED",
            "description": "RUB",
            "date": "2019-01-01T00:00:00",
            "operationAmount": {
                "amount": "1",
                "currency": {"code": "RUB"},
            },
            "to": "Счет 1111",
        },
        {
            "state": "EXECUTED",
            "description": "USD",
            "date": "2019-01-02T00:00:00",
            "operationAmount": {
                "amount": "2",
                "currency": {"code": "USD"},
            },
            "to": "Счет 2222",
        },
    ]
    monkeypatch.setattr(
        main_module, "read_transactions_json", lambda p: data
    )
    _feed_inputs(monkeypatch, ["1", "EXECUTED", "нет", "да", "нет"])

    main_module.main()
    out = capsys.readouterr().out
    assert "Всего банковских операций в выборке: 1" in out
    assert "Сумма: 1 руб." in out
    assert "Сумма: 2 USD" not in out


def test_main_search_by_word(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Поиск по слову в описании через process_bank_search."""
    data = [
        {"state": "EXECUTED", "description": "Перевод", "date": "x"},
        {"state": "EXECUTED", "description": "Вклад", "date": "x"},
    ]
    monkeypatch.setattr(
        main_module, "read_transactions_json", lambda p: data
    )
    _feed_inputs(
        monkeypatch,
        ["1", "EXECUTED", "нет", "нет", "да", "Перевод"],
    )

    main_module.main()
    out = capsys.readouterr().out
    assert "Всего банковских операций в выборке: 1" in out
