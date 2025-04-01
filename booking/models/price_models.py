from django.db import models
from datetime import datetime
from .space_models import Space  # Импорт моделей Space и Option



class PriceAbstract (models.Model):
    date_new_price = models.DateField(default=datetime.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.price} руб/час с {self.date_new_price}'


class PriceSpace (PriceAbstract):
    space_id = models.ForeignKey(to='Space', on_delete=models.CASCADE,
                                 related_name='price_of_space')

    class Meta:
        verbose_name = "Цены на помещения"


