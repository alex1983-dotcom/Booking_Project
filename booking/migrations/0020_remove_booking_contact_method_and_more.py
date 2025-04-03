# Generated by Django 5.1.7 on 2025-04-02 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0019_alter_feedback_options_booking_contact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='contact_method',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='promo_code',
        ),
        migrations.AddField(
            model_name='feedback',
            name='promo_code',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Промокод'),
        ),
    ]
