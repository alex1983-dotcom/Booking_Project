from rest_framework import serializers
from .models import Space, Booking

class SpaceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Space.
    """
    class Meta:
        model = Space
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Booking.
    """
    class Meta:
        model = Booking
        fields = '__all__'
