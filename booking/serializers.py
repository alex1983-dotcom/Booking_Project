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
    promo_code = serializers.CharField(
        source='contact.promo_code', 
        read_only=True
    )  # Промокод подтягивается из связанной модели Feedback

    def validate(self, data):
        """
        Проверка на валидность дат.
        """
        if data['event_start_date'] >= data['event_end_date']:
            raise serializers.ValidationError(
                "Дата начала должна быть раньше даты окончания."
            )
        return data

    class Meta:
        model = Booking
        fields = [
            'space',
            'event_start_date',
            'event_end_date',
            'guests_count',
            'preferences',
            'contact',
            'promo_code',  # Read-only поле
        ]


class PreferenceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели AdditionalPreference.
    """
    class Meta:
        model = AdditionalPreference
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Feedback.
    """
    id = serializers.IntegerField(read_only=True)
    call_time = serializers.TimeField(allow_null=True, required=False)  # Разрешаем `null`

    class Meta:
        model = Feedback
        fields = ['id', 'name', 'phone_number', 'call_time', 'promo_code', 'messengers']
