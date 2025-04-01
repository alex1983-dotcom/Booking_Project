from django.db import models
from datetime import datetime
from .space_models import Space  
from django.core.exceptions import ValidationError


class AdditionalPreference(models.Model):
    name = models.CharField(max_length=50, verbose_name='Дополнительные опции')

    def delete(self, *args, **kwargs):
        from booking.models import Booking
        if Booking.objects.filter(preferences__id=self.id).exists():
            raise Exception("Невозможно удалить дополнительные опции, оно используется в бронированиях.")
        super().delete(*args, **kwargs)
    
    
    
    class Meta:
        verbose_name = "Дополнительные опции"
        verbose_name_plural = "Дополнительные опции"
    
    def __str__(self):
            return self.name

class Feedback(models.Model):
    """Модель для обратной связи(контакты для связи, которые оставляет заказчик)"""
    class Messenger(models.IntegerChoices):
        VIBER = 1, 'Viber'
        TELEGRAM = 2, 'Telegram'
        WHATSAPP = 3, 'WhatsApp'
    
    name = models.CharField(max_length=255, verbose_name='Имя')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Электронная почта')
    messengers = models.IntegerField(
        choices=Messenger.choices,
        default=Messenger.VIBER,
        verbose_name="Мессенджер"
    )

    class Meta:
        verbose_name = "Контакт заказчика"
        verbose_name_plural = "Контакты заказчика"

    def __str__(self):
      return f"{self.name} - {self.phone_number}"  

class Booking(models.Model):
    """
    Модель, представляющая бронирование.
    """
    class BookingStatus(models.IntegerChoices):
        AVAILABLE = 1, 'Свободно'
        BOOKED = 2, 'Забронировано'

    space = models.ForeignKey(Space, on_delete=models.SET_NULL, null=True, verbose_name='Пространство')  # Связь с пространством
    event_start_date = models.DateTimeField(default=datetime.now, verbose_name='Дата начала')  # Дата и время начала бронирования
    event_end_date = models.DateTimeField(verbose_name='Дата окончания')  # Дата и время окончания бронирования
    event_format = models.CharField(max_length=100, verbose_name='Формат мероприятия')  # Формат мероприятия
    guests_count = models.PositiveIntegerField(verbose_name='Количество гостей')  # Количество гостей
    preferences = models.ManyToManyField(AdditionalPreference, blank=True, verbose_name='Дополнительные опции')  # Дополнительные предпочтения
    promo_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='Промокод')  # Промокод (опционально)
    contact_method = models.CharField(max_length=50, verbose_name='Контактные данные')  # Контактные данные
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')  # Дата создания записи
    status = models.IntegerField(
        choices=BookingStatus.choices,
        default=BookingStatus.AVAILABLE,
        verbose_name="Статус"
    )
    contact = models.ForeignKey(
        Feedback,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Контакт заказчика'
    )

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['event_start_date']

    def __str__(self):
        return f"Бронирование {self.space.name} с {self.event_start_date.strftime('%d.%m.%Y %H:%M')} по {self.event_end_date.strftime('%d.%m.%Y %H:%M')} | Статус: {self.get_status_display()}"

    def get_status_display(self):
        return dict(self.BookingStatus.choices).get(self.status, 'Неизвестно')

   
    def clean(self):
        """
        Проверяем, что количество гостей не превышает вместимость пространства.
        """
        if self.space and self.guests_count > self.space.capacity:
            raise ValidationError(
                f"Количество гостей ({self.guests_count}) превышает вместимость пространства ({self.space.capacity})."
            )
        






