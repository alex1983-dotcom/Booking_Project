# Generated by Django 5.1.7 on 2025-04-04 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0020_remove_booking_contact_method_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='event_format',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Формат мероприятия'),
        ),
    ]
