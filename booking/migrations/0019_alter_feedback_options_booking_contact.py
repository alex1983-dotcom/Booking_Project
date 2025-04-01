# Generated by Django 5.1.7 on 2025-04-01 20:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0018_feedback'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feedback',
            options={'verbose_name': 'Контакт заказчика', 'verbose_name_plural': 'Контакты заказчика'},
        ),
        migrations.AddField(
            model_name='booking',
            name='contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='booking.feedback', verbose_name='Контакт заказчика'),
        ),
    ]
