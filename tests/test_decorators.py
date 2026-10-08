# test_decorators.py
from unittest.mock import mock_open, patch

import pytest

from src.decorators import log


@log()
def add(a: int, b: int) -> int:
    return a + b


@log()
def div(a: float, b: float) -> float:
    return a / b


@log(filename="test.log")
def multiply(a: int, b: int) -> int:
    return a * b


@log(filename="test.log")
def failing_func(x: int) -> None:
    raise ValueError("Invalid value")


def test_log_console_success(caplog: pytest.LogCaptureFixture) -> None:
    """Тест успешного вызова с выводом в консоль (через logging)."""
    result = add(2, 3)
    assert result == 5
    assert "Calling add(2, 3)" in caplog.text
    assert "add returned 5" in caplog.text


def test_log_console_exception(caplog: pytest.LogCaptureFixture) -> None:
    """Тест вызова с исключением, логи в консоль."""
    with pytest.raises(ZeroDivisionError):
        div(5, 0)
    assert "Calling div(5, 0)" in caplog.text
    assert "div raised ZeroDivisionError" in caplog.text
    assert "args: 5, 0" in caplog.text


def test_log_file_success() -> None:
    """Тест успешного вызова с записью в файл (используем mock)."""
    m = mock_open()
    with patch("builtins.open", m):
        result = multiply(4, 5)
        assert result == 20

        args, kwargs = m.call_args
        assert args[0].endswith("test.log")
        assert args[1] == 'a'
        assert kwargs.get('encoding') == 'utf-8'

        write_calls = [call[0][0] for call in m().write.call_args_list]
        assert any("Calling multiply(4, 5)" in msg for msg in write_calls)
        assert any("multiply returned 20" in msg for msg in write_calls)


def test_log_file_exception() -> None:
    """Тест вызова с исключением, запись в файл (используем mock)."""
    m = mock_open()
    with patch("builtins.open", m):
        with pytest.raises(ValueError):
            failing_func(42)

        args, kwargs = m.call_args
        assert args[0].endswith("test.log")
        assert args[1] == 'a'
        assert kwargs.get('encoding') == 'utf-8'

        write_calls = [call[0][0] for call in m().write.call_args_list]
        assert any("Calling failing_func(42)" in msg for msg in write_calls)
        assert any("failing_func raised ValueError" in msg for msg in write_calls)
        assert any("args: 42" in msg for msg in write_calls)


def test_log_with_kwargs(caplog: pytest.LogCaptureFixture) -> None:
    """Тест с именованными аргументами."""
    @log()
    def greet(name: str, greeting: str = "Hello") -> str:
        return f"{greeting}, {name}!"

    result = greet("Alice", greeting="Hi")
    assert result == "Hi, Alice!"
    assert "Calling greet('Alice', greeting='Hi')" in caplog.text
    assert "greet returned 'Hi, Alice!'" in caplog.text
