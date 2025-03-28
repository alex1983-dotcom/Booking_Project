# from django.db import models
from . import *


class PriceAbstract (models.Model):
    date_new_price = models.DateField(default=datetime.datetime.now)
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


class PriceOption (PriceAbstract):
    option_id = models.ForeignKey(to='Option', on_delete=models.CASCADE,
                                  related_name='price_of_option')

    class Meta:
        verbose_name = 'Цены на дополнительные услуги'
