from django.urls import path
from .views import SpaceListView, BookingCreateView, EquipmentListView, ParkingListView, SpaceDetailView, BookingListView

urlpatterns = [
    path('api/spaces/', SpaceListView.as_view(), name='list-spaces'),           # Для списка залов
    path('api/spaces/<int:pk>/', SpaceDetailView.as_view(), name='detail-space'),
    path('api/bookings/', BookingListView.as_view(), name='list-bookings'),     # Для списка бронирований (GET)
    path('api/bookings/create/', BookingCreateView.as_view(), name='create-booking'),  # Для создания бронирования (POST)
    path('api/equipments/', EquipmentListView.as_view(), name='list-equipments'),
    path('api/parkings/', ParkingListView.as_view(), name='list-parkings'),
]

