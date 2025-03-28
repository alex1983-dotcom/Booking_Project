from rest_framework import serializers
from .models import Space, Booking

class SpaceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Space.
    """
    class Meta:
        model = Space
        fields = '__all__'

from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'space',
            'event_start_date',
            'event_end_date',
            'event_format',
            'guests_count',
            'preferences',
            'promo_code',
            'contact_method'
        ]