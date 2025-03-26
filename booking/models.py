from django.db import models
import datetime

class Space(models.Model):
    """
    Модель, представляющая пространство для бронирования.
    """
    name = models.CharField(max_length=100)  # Название пространства
    capacity = models.PositiveIntegerField()  # Вместимость пространства
    available = models.BooleanField(default=True)  # Статус доступности пространства

    class Meta:
        verbose_name = "Пространство"
        verbose_name_plural = "Пространства"
        ordering = ['name']

    def __str__(self):
        return self.name

class Booking(models.Model):
    """
    Модель, представляющая бронирование.
    """
    space = models.ForeignKey(Space, on_delete=models.CASCADE)  # Связь с пространством
    event_start_date = models.DateTimeField(default=datetime.datetime.now)  # Импортируйте datetime
  # Дата и время начала бронирования
    event_end_date = models.DateTimeField()  # Дата и время окончания бронирования
    event_format = models.CharField(max_length=100)  # Формат мероприятия
    guests_count = models.PositiveIntegerField()  # Количество гостей
    preferences = models.JSONField()  # Дополнительные предпочтения
    promo_code = models.CharField(max_length=50, blank=True, null=True)  # Промокод (опционально)
    contact_method = models.CharField(max_length=50)  # Метод связи
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания записи

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['event_start_date']

    def __str__(self):
        return f"Бронирование {self.space.name} с {self.event_start_date} по {self.event_end_date}"
