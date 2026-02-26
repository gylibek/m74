from src import widget

# Импортируем модуль


# Пример использования функций
def main() -> None:

    # Тестовые данные для маскировки
    card_input = "Visa Platinum 7000792289606361"
    masked_card = widget.mask_account_card(card_input)
    print(f"Исходная карта: {card_input}")
    print(f"Замаскированная карта: {masked_card}")
    # Тестовые данные для даты
    date_input = "2024-03-11T02:26:18.671407"
    formatted_date = widget.get_date(date_input)
    print(f"\nИсходная дата: {date_input}")
    print(f"Форматированная дата: {formatted_date}")


if __name__ == "__main__":
    main()


def display_results() -> None:
    # Пример с форматированием
    card_examples = [
        "Visa Platinum 7000792289606361",
        "Maestro 7000792289606361",
        "Счет 73654108430135874305"
    ]

    date_examples = [
        "2024-03-11T02:26:18.671407",
        "2023-12-25T23:59:59.999999",
        "2025-01-01T00:00:00.000000"
    ]

    print("Результаты работы функции маскировки:")
    print("-------------------------------------")
    for card in card_examples:
        print(f"Исходная: {card}")
        print(f"Результат: {widget.mask_account_card(card)}\n")

    print("Результаты работы функции форматирования даты:")
    print("---------------------------------------------")
    for date in date_examples:
        print(f"Исходная: {date}")
        print(f"Результат: {widget.get_date(date)}\n")


if __name__ == "__main__":
    display_results()
