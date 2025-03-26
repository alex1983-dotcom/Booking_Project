from django.contrib import admin
from .models import Space, Booking

class BookingInline(admin.TabularInline):
    """
    Inline-редактор для модели Booking.
    """
    model = Booking
    extra = 1  # Количество пустых форм для создания новых записей

@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    """
    Админка для модели Space.
    """
    list_display = ('name', 'capacity', 'available')  # Отображаемые поля
    search_fields = ('name',)  # Поле поиска
    list_filter = ('available',)  # Фильтры
    inlines = [BookingInline]  # Подключение inline-редактора

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Админка для модели Booking.
    """
    list_display = ('space', 'event_start_date', 'event_end_date', 'event_format', 'guests_count', 'contact_method')
    search_fields = ('space__name', 'event_format')  # Поля поиска
    list_filter = ('event_start_date', 'space')  # Фильтры
    ordering = ('event_start_date',)  # Сортировка
