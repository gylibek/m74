from datetime import datetime


def filter_by_state(data, state='EXECUTED'):
    """
    Фильтрация данных по статусу state

    :param data: список словарей с данными
    :param state: значение состояния для фильтрации (по умолчанию 'EXECUTED')
    :return: отфильтрованный список словарей
    """
    return [item for item in data if item.get('state') == state]
