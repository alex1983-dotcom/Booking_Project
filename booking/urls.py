from django.urls import path
from .views import CheckAvailabilityAPIView, CreateBookingAPIView, PreferencesAPIView

urlpatterns = [
    path('check-availability/', CheckAvailabilityAPIView.as_view(), name='check-availability'),
    path('create-booking/', CreateBookingAPIView.as_view(), name='create-booking'),
    # Дополнительный эндпоинт для обработки доступных предпочтений
    path('get-preferences/', PreferencesAPIView.as_view(), name='get-preferences'),
]


