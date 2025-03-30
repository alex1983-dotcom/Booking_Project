# bot/urls.py
from django.urls import path
from .views import TelegramWebhookView
from .views_bitrix_24 import handle_order  # Импорт обработчика
urlpatterns = [
    path('webhook/', TelegramWebhookView.as_view(), name='telegram-webhook'),
    path('api/bitrix24/order/', handle_order, name='handle_order'),
]
