from django import forms
from django.contrib import admin
from .models.space_models import Space, Option
from .models.booking_models import Booking, Preference
from .models.price_models import PriceSpace, PriceOption

@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'capacity', 'area')  # Убедитесь, что эти поля существуют в модели Space
    search_fields = ('name',)
    list_filter = ('capacity', 'area')

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'all_count')  # Используйте правильные поля из модели Option
    search_fields = ('name',)
    list_filter = ('all_count',)

@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Отображает ID и имя предпочтений
    search_fields = ('name',)  # Поиск по имени


# Пользовательская форма для Booking
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'  # Включает все поля модели

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    form = BookingForm  # Подключаем пользовательскую форму
    list_display = ('id', 'space', 'event_start_date', 'event_end_date', 'guests_count', 'status')  # Отображаемые поля
    search_fields = ('space__name', 'event_format')
    list_filter = ('event_start_date', 'status')
    filter_horizontal = ('preferences',)  # Удобный интерфейс для выбора предпочтений

@admin.register(PriceSpace)
class PriceSpaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'space_id', 'price', 'date_new_price')  # Убедитесь, что используете существующие поля
    search_fields = ('space_id__name',)
    list_filter = ('date_new_price',)

@admin.register(PriceOption)
class PriceOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'option_id', 'price', 'date_new_price')  # Используйте поля из модели PriceOption
    search_fields = ('option_id__name',)
    list_filter = ('date_new_price',)
