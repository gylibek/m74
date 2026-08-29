# test_decorators.py
import pytest
import os
from src.decorators import log


# Тестируемая функция
@log()
def add(a, b):
    return a + b


@log()
def div(a, b):
    return a / b


@log(filename="test.log")
def multiply(a, b):
    return a * b


@log(filename="test.log")
def failing_func(x):
    raise ValueError("Invalid value")


def test_log_console_success(capsys):
    """Тест успешного вызова с выводом в консоль."""
    result = add(2, 3)
    assert result == 5
    captured = capsys.readouterr()
    out = captured.out
    assert "Calling add(2, 3)" in out
    assert "add returned 5" in out


def test_log_console_exception(capsys):
    """Тест вызова с исключением, логи в консоль."""
    with pytest.raises(ZeroDivisionError):
        div(5, 0)
    captured = capsys.readouterr()
    out = captured.out
    assert "Calling div(5, 0)" in out
    assert "div raised ZeroDivisionError" in out
    assert "args: 5, 0" in out


def test_log_file_success():
    """Тест успешного вызова с записью в файл."""
    # Удаляем файл перед тестом, если существует
    if os.path.exists("test.log"):
        os.remove("test.log")

    result = multiply(4, 5)
    assert result == 20

    # Проверяем содержимое файла
    with open("test.log", "r", encoding="utf-8") as f:
        content = f.read()
    assert "Calling multiply(4, 5)" in content
    assert "multiply returned 20" in content

    # Очистка после теста
    os.remove("test.log")


def test_log_file_exception():
    """Тест вызова с исключением, запись в файл."""
    if os.path.exists("test.log"):
        os.remove("test.log")

    with pytest.raises(ValueError):
        failing_func(42)

    with open("test.log", "r", encoding="utf-8") as f:
        content = f.read()
    assert "Calling failing_func(42)" in content
    assert "failing_func raised ValueError" in content
    assert "args: 42" in content

    os.remove("test.log")


def test_log_with_kwargs(capsys):
    """Тест с именованными аргументами."""
    @log()
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}!"

    result = greet("Alice", greeting="Hi")
    assert result == "Hi, Alice!"
    captured = capsys.readouterr()
    out = captured.out
    assert "Calling greet('Alice', greeting='Hi')" in out
    assert "greet returned 'Hi, Alice!'" in out
