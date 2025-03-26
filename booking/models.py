from django.db import models

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
        ordering = ['name']  # Сортировка по имени

    def __str__(self):
        return self.name

class Booking(models.Model):
    """
    Модель, которая представляет бронирование.
    """
    space = models.ForeignKey(Space, on_delete=models.CASCADE)  # Связь с пространством
    event_date = models.DateTimeField()  # Дата и время мероприятия
    event_format = models.CharField(max_length=100)  # Формат мероприятия
    guests_count = models.PositiveIntegerField()  # Количество гостей
    preferences = models.JSONField()  # Дополнительные предпочтения
    promo_code = models.CharField(max_length=50, blank=True, null=True)  # Промокод (опционально)
    contact_method = models.CharField(max_length=50)  # Метод связи
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания записи

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['event_date']  # Сортировка по дате мероприятия

    def __str__(self):
        return f"Бронирование {self.space.name} на {self.event_date}"

