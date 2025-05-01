from django.db import models
from datetime import datetime


class AdditionalPreference(models.Model):
    """
    Модель для дополнительных предпочтений.
    """
    name = models.CharField(max_length=50, verbose_name='Дополнительные опции')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Дополнительные опции"
        verbose_name_plural = "Дополнительные опции"


class Feedback(models.Model):
    """
    Модель для обратной связи (контакты для связи заказчика).
    """
    class Messenger(models.IntegerChoices):
        NOT_SPECIFIED = 0, 'Не указан'  # Добавляем значение по умолчанию
        VIBER = 1, 'Viber'
        TELEGRAM = 2, 'Telegram'
        WHATSAPP = 3, 'WhatsApp'

    name = models.CharField(max_length=255, verbose_name='Имя')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    call_time = models.TimeField(verbose_name='Время звонка')
    promo_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='Промокод')
    messengers = models.IntegerField(
        choices=Messenger.choices,
        null=False,  # Запрещаем null, чтобы всегда было значение
        blank=False,  # Запрещаем пустые строки
        default=Messenger.NOT_SPECIFIED,  # Используем 0 для "Не указан"
        verbose_name="Мессенджер"
    )

    def __str__(self):
        return f"{self.name} - {self.phone_number}"

    class Meta:
        verbose_name = "Контакт заказчика"
        verbose_name_plural = "Контакты заказчика"


class Booking(models.Model):
    """
    Модель, представляющая бронирование.
    """
    class BookingStatus(models.IntegerChoices):
        AVAILABLE = 1, 'Свободно'
        BOOKED = 2, 'Забронировано'

    space = models.ForeignKey('Space', on_delete=models.SET_NULL, null=True, verbose_name='Пространство')
    event_start_date = models.DateTimeField(default=datetime.now, verbose_name='Дата начала')
    event_end_date = models.DateTimeField(verbose_name='Дата окончания')
    event_format = models.CharField(max_length=100, blank=True, null=True, verbose_name='Формат мероприятия')
    guests_count = models.PositiveIntegerField(verbose_name='Количество гостей')
    preferences = models.ManyToManyField(AdditionalPreference, blank=True, verbose_name='Дополнительные опции')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
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

    def __str__(self):
        return (
            f"Бронирование | {self.space.name} | с {self.event_start_date.strftime('%d.%m.%Y %H:%M')} "
            f"по {self.event_end_date.strftime('%d.%m.%Y %H:%M')} | Статус: {self.get_status_display()}"
        )

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['event_start_date']









