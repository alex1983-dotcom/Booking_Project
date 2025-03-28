from django.db import models
import datetime


class Space(models.Model):
    """
    Модель, представляющая пространство для бронирования.
    """
    name = models.CharField(max_length=100)  # Название пространства
    capacity = models.PositiveIntegerField()  # Вместимость пространства
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # Цена в час
    area = models.PositiveIntegerField(default=0) # Полощадь пространства в метрах квадратных
    class Meta:
        verbose_name = "Пространство"
        verbose_name_plural = "Пространства"
        ordering = ['name']
        # app_label = 'models'

    def __str__(self):
        return f"{self.name} - {self.area} м.кв. - {self.price_per_hour} BYN/час"
