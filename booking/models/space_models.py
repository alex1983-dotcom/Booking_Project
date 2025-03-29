from django.db import models



class AbstractItem(models.Model):
    """
    Общие свойства для моделей помещений и доп. опций
    """
    name = models.CharField(max_length=20, default='test_name',
                            help_text='Название', verbose_name='Название')  # Название
    description = models.TextField(default='test_description',
                                   help_text='Описание', verbose_name='Описание') # Описание

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return f'{self.name}: {self.description[:20]}...'

class Space(AbstractItem):
    """
    Модель, представляющая пространство для бронирования.
    """
    capacity = models.PositiveIntegerField(default=1)  # Вместимость пространства
    area = models.PositiveIntegerField(default=1) # Полощадь в метрах квадратных

    class Meta:
        verbose_name = "Пространство"
        verbose_name_plural = "Пространства"


class Option(AbstractItem):
    all_count = models.PositiveIntegerField(default=1, help_text='Количество', verbose_name='Количество')

    class Meta:
        verbose_name = 'Дополнительная опция'
        verbose_name_plural = 'Дополнительные опции'