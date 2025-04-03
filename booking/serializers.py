from rest_framework import serializers
from .models import Space, Booking, AdditionalPreference, Feedback

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

class PreferenceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели AdditionalPreference.
    """
    class Meta:
        model = AdditionalPreference
        fields = '__all__'



class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'name', 'phone_number', 'email', 'promo_code', 'messengers']
