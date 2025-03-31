from django.http import JsonResponse
from .utils import send_order_to_bitrix  # Импорт вспомогательной функции

# Пример Вьюхи
# Нужны данные от сервиса на Bitrix24--(webhook-id и webhook-code)
# Нужен ID чат клиента
def handle_order(request):
    """
    Обрабатывает поступающие заказы и отправляет их в Bitrix24.
    """
    if request.method == "POST":
        # Получение данных из запроса
        order_data = request.POST.get("order_data", "Нет данных о заказе")
        chat_id = request.POST.get("chat_id", "12345")  # ID чата клиента
        webhook_url = "https://client-bitrix24-domain/rest/webhook_id/webhook_code"

        # Отправка данных в Bitrix24
        response = send_order_to_bitrix(chat_id, order_data, webhook_url)
        return JsonResponse({"status": "success", "response": response})
    return JsonResponse({"status": "error", "message": "Invalid request method"})

