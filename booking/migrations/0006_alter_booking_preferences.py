# Generated by Django 5.1.7 on 2025-03-29 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_option_alter_space_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='preferences',
            field=models.JSONField(default='Не указано', verbose_name='Предпочтения'),
        ),
    ]
