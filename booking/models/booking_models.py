from django.db import models
from datetime import datetime
from .space_models import Space  


class Preference(models.Model):
    """
    Модель предпочтений для бронирования.
    """
    name = models.CharField(max_length=50, verbose_name='Предпочтение')

    def __str__(self):
        return self.name
    

class Booking(models.Model):
    """
    Модель, представляющая бронирование.
    """
    class BookingStatus(models.IntegerChoices):
        AVAILABLE = 1, 'Свободно'
        BOOKED = 2, 'Забронировано'

    space = models.ForeignKey(Space, on_delete=models.CASCADE, verbose_name='Пространство')  # Связь с пространством
    event_start_date = models.DateTimeField(default=datetime.now, verbose_name='Дата начала')  # Дата и время начала бронирования
    event_end_date = models.DateTimeField(verbose_name='Дата окончания')  # Дата и время окончания бронирования
    event_format = models.CharField(max_length=100, verbose_name='Формат мероприятия')  # Формат мероприятия
    guests_count = models.PositiveIntegerField(verbose_name='Количество гостей')  # Количество гостей
    preferences = models.ManyToManyField(Preference, verbose_name='Предпочтения')  # Дополнительные предпочтения
    promo_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='Промокод')  # Промокод (опционально)
    contact_method = models.CharField(max_length=50, verbose_name='Контактные данные')  # Контактные данные
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')  # Дата создания записи
    status = models.IntegerField(
        choices=BookingStatus.choices,
        default=BookingStatus.AVAILABLE,
        verbose_name="Статус"
    )

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['event_start_date']

    def __str__(self):
        return f"Бронирование {self.space.name} с {self.event_start_date.strftime('%d.%m.%Y %H:%M')} по {self.event_end_date.strftime('%d.%m.%Y %H:%M')} | Статус: {self.get_status_display()}"

    def get_status_display(self):
        return dict(self.BookingStatus.choices).get(self.status, 'Неизвестно')
