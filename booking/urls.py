from django.urls import path
from .views import CheckAvailabilityAPIView, CreateBookingAPIView

urlpatterns = [
    path('check-availability/', CheckAvailabilityAPIView.as_view(), name='check-availability'),
    path('create-booking/', CreateBookingAPIView.as_view(), name='create-booking'),
]

