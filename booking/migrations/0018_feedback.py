# Generated by Django 5.1.7 on 2025-04-01 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0017_remove_priceoption_option_id_delete_option_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Номер телефона')),
                ('email', models.EmailField(max_length=254, verbose_name='Электронная почта')),
                ('messengers', models.IntegerField(choices=[(1, 'Viber'), (2, 'Telegram'), (3, 'WhatsApp')], default=1, verbose_name='Мессенджер')),
            ],
            options={
                'verbose_name': 'Обратная связь',
                'verbose_name_plural': 'Обратные связи',
            },
        ),
    ]
