---

## Новый функционал

### Декоратор `@log`
Декоратор для автоматического логирования вызовов функций.  
**Возможности:**
- Логирует время начала и окончания выполнения.
- Записывает переданные аргументы и возвращаемое значение.
- Перехватывает исключения и логирует информацию об ошибке (тип, аргументы, время выполнения до ошибки).
- Вывод в консоль (по умолчанию) или в файл (если указан параметр `filename`).

**Пример использования:**
```python
from src.decorators import log

@log()  # логи в консоль
def add(a, b):
    return a + b

@log(filename="app.log")  # логи в файл app.log
def multiply(a, b):
    return a * b
```

**Пример вывода в консоль:**
```
2025-02-13 12:34:56,789 - add - INFO - Calling add(2, 3)
2025-02-13 12:34:56,790 - add - INFO - add returned 5 in 0.0010 sec
```

При возникновении ошибки:
```
2025-02-13 12:34:57,123 - div - ERROR - div raised ZeroDivisionError: division by zero (args: 5, 0, kwargs: ) after 0.0002 sec
```

---

### Модуль `processing`
Содержит функции для обработки списков словарей:

- **`filter_by_state(data, state='EXECUTED')`**  
  Фильтрует список словарей по значению ключа `state`.  
  Пример:
  ```python
  from src.processing import filter_by_state
  data = [{'state': 'EXECUTED', 'id': 1}, {'state': 'CANCELED', 'id': 2}]
  filtered = filter_by_state(data)  # возвращает [{'state': 'EXECUTED', 'id': 1}]
  ```

- **`sort_by_date(data, descending=True)`**  
  Сортирует список словарей по ключу `date` (формат `%Y-%m-%dT%H:%M:%S.%f`).  
  По умолчанию сортировка по убыванию (`descending=True`).  
  Пример:
  ```python
  from src.processing import sort_by_date
  data = [{'date': '2023-01-01T10:00:00.000000'}, {'date': '2023-02-01T10:00:00.000000'}]
  sorted_data = sort_by_date(data)  # сначала более поздняя дата
  ```

---

### Тестирование и покрытие

Для запуска тестов и проверки покрытия кода используйте `pytest` с плагином `pytest-cov`.

**Установка зависимостей для тестирования:**
```bash
pip install pytest pytest-cov
```

**Запуск тестов с отчётом о покрытии:**
```bash
python -m pytest --cov=src --cov-report=term-missing tests/
```

**Генерация HTML-отчёта по покрытию:**
```bash
python -m pytest --cov=src --cov-report=html tests/
```
Отчёт будет сохранён в папку `htmlcov/` – откройте `index.html` в браузере для детального просмотра.

**Настройка минимального порога покрытия** (например, 80%):
```bash
python -m pytest --cov=src --cov-fail-under=80 tests/
```

---