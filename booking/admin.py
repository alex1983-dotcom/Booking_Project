from django import forms
from django.contrib import admin
from .models.space_models import Space
from .models.booking_models import Booking, AdditionalPreference, Feedback
from .models.price_models import PriceSpace
from .forms import FeedbackAdminForm,BookingForm

@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'capacity', 'area') 
    search_fields = ('name',)
    list_filter = ('capacity', 'area')

@admin.register(AdditionalPreference)
class AdditionalPreferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name') 
    search_fields = ('name',) 

# Пользовательская форма для Booking
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__' 

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    form = BookingForm  # Подключаем пользовательскую форму
    list_display = ('id', 'space', 'created_at', 'contact', 'event_start_date', 'event_end_date', 'guests_count', 'status')
    search_fields = ('space__name', 'event_format')
    list_filter = ('event_start_date', 'status')
    filter_horizontal = ('preferences',)  # Интерфейс для выбора предпочтений

@admin.register(PriceSpace)
class PriceSpaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'space_id', 'price', 'date_new_price') 
    search_fields = ('space_id__name',)
    list_filter = ('date_new_price',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    form = FeedbackAdminForm  

    def get_messenger_display(self, obj):
        return obj.get_messengers_display()

    list_display = ('id', 'name', 'phone_number', 'promo_code', 'get_messenger_display', 'call_time')
    search_fields = ('name', 'phone_number', 'promo_code', 'call_time')
