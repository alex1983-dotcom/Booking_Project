from django.db import models

class Space(models.Model):
    """
    Модель для помещений (пространств).
    Здесь описывается только информация о зале.
    """
    name = models.CharField(max_length=255, verbose_name="Название зала")
    area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Площадь (м²)")
    capacity = models.PositiveIntegerField(verbose_name="Количество мест")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за час (BYN)")
    floor = models.PositiveIntegerField(verbose_name="Этаж", null=True, blank=True)
    description = models.TextField(verbose_name="Описание зала", null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Помещение"
        verbose_name_plural = "Помещения"

    def __str__(self):
        return self.name


class Booking(models.Model):
    """
    Модель для бронирования.
    Все даты бронирования (начало и окончание) вводятся в этой модели.
    """
    space = models.ForeignKey(Space, on_delete=models.CASCADE, verbose_name="Зал")
    user_name = models.CharField(max_length=255, verbose_name="Имя пользователя")
    user_contact = models.CharField(max_length=255, verbose_name="Контакт пользователя")
    date = models.DateTimeField(verbose_name="Дата начала бронирования")
    end_date = models.DateTimeField(verbose_name="Дата окончания бронирования")
    duration = models.PositiveIntegerField(verbose_name="Продолжительность (часов)", null=True, blank=True)
    confirmed = models.BooleanField(default=True, verbose_name="Подтверждено")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        return f"{self.user_name} забронировал зал {self.space.name} начиная с {self.date:%d.%m.%Y %H:%M}"

    def save(self, *args, **kwargs):
        # Если пользователь ввёл обе даты, можно автоматически вычислить поле duration,
        # чтобы оно отображало разницу в часах между end_date и date.
        if self.date and self.end_date:
            from datetime import timedelta
            delta = self.end_date - self.date
            self.duration = int(delta.total_seconds() // 3600)
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        """
        Итоговая стоимость бронирования = продолжительность * цена за час зала.
        """
        if self.duration and self.space and self.space.price:
            return self.duration * self.space.price
        return None



class Equipment(models.Model):
    """
    Модель для оборудования.
    Каждое оборудование привязано к определённому помещению.
    """
    space = models.ForeignKey(
        Space,
        on_delete=models.CASCADE,
        related_name='equipments',
        verbose_name="Пространство"
    )
    name = models.CharField(max_length=255, verbose_name="Название оборудования")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        ordering = ['name']
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"

    def __str__(self):
        return f"{self.name} ({self.space.name})"


from django.db import models
from datetime import timedelta

class Booking(models.Model):
    space = models.ForeignKey('booking.Space', on_delete=models.CASCADE, verbose_name="Помещение")
    user_name = models.CharField(max_length=255, verbose_name="Имя пользователя")
    user_contact = models.CharField(max_length=255, verbose_name="Контакт пользователя")
    date = models.DateTimeField(verbose_name="Дата начала бронирования")
    end_date = models.DateTimeField(verbose_name="Дата окончания бронирования", null=True, blank=True)
    duration = models.PositiveIntegerField(verbose_name="Продолжительность (часов)", null=True, blank=True)
    confirmed = models.BooleanField(default=True, verbose_name="Подтверждено")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        return f"{self.user_name} забронировал {self.space.name} на {self.date.strftime('%d.%m.%Y %H:%M')}"

    def save(self, *args, **kwargs):
        # Если заданы обе даты, вычисляем продолжительность в часах
        if self.date and self.end_date:
            delta = self.end_date - self.date
            # Округляем вниз до целого числа часов
            self.duration = int(delta.total_seconds() // 3600)
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        """
        Вычисляемая итоговая цена бронирования:
         продолжительность (в часах) * цена за час в помещении.
        Предполагается, что self.space.price – число (BYN за час).
        """
        if self.duration and self.space and self.space.price:
            return self.duration * self.space.price
        return None





class Parking(models.Model):
    """
    Модель для парковки.
    Содержит информацию: название парковки, является ли парковка платной и цена за час (если платная).
    """
    name = models.CharField(max_length=255, verbose_name="Название парковки")
    is_paid = models.BooleanField(default=False, verbose_name="Платная парковка")
    price_per_hour = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Цена за час (BYN)"
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Парковка"
        verbose_name_plural = "Парковки"

    def __str__(self):
        return self.name
