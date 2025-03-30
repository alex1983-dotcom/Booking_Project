def some_helper_function():
    # Пример вспомогательной функции
    pass


# Нужны данные от сервиса на Bitrix24--(webhook-id и webhook-code)
import requests

def send_order_to_bitrix(chat_id, message, webhook_url):
    """
    Отправляет сообщение в чат клиента Bitrix24 через Webhook.

    :param chat_id: ID чата клиента
    :param message: Текст сообщения
    :param webhook_url: URL вебхука
    :return: Ответ API Bitrix24
    """
    url = f"{webhook_url}/im.message.add"  # Метод для отправки сообщений
    payload = {
        "CHAT_ID": chat_id,
        "MESSAGE": message
    }
    response = requests.post(url, json=payload)
    return response.json()


