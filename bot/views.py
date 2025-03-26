# bot/views.py
from django.views import View
from django.http import JsonResponse
from booking.models import Space, Booking  # импорт из booking!

class TelegramWebhookView(View):
    def post(self, request, *args, **kwargs):
        # логика для обработки webhook от Telegram
        return JsonResponse({"status": "ok"})
