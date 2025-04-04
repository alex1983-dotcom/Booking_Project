from django.db import models

class AbstractItem(models.Model):
    """
    Общие свойства для моделей помещений и доп. опций
    """
    name = models.CharField(max_length=20, default='Не указано',
                            help_text='Название', verbose_name='Название')  # Название
    description = models.TextField(default='Не указано',
                                   help_text='Описание', verbose_name='Описание') # Описание

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'

class Space(AbstractItem):
    """
    Модель, представляющая пространство для бронирования.
    """
    capacity = models.PositiveIntegerField(default=1, help_text='Количество мест', 
                                           verbose_name='Количество мест')  # Вместимость пространства
    area = models.PositiveIntegerField(default=1, help_text='Площадь', 
                                       verbose_name='Площадь') # Полощадь в метрах квадратных

    class Meta:
        verbose_name = "Пространство"
        verbose_name_plural = "Пространства"


