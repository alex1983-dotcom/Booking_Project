from django.contrib import admin
from .models import Space, Equipment, Booking, Parking

# Определяем Inline-класс для отображения оборудования в виде таблицы на странице редактирования Space
class EquipmentInline(admin.TabularInline):
    model = Equipment
    extra = 1  # число пустых форм для добавления нового оборудования
    fields = ('name', 'description')
    # Вы можете настроить дополнительные параметры, например, readonly_fields, если необходимо

@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'area', 'capacity', 'price', 'floor')
    search_fields = ('name',)
    list_filter = ('floor',)
    ordering = ('name',)
    list_per_page = 25
    inlines = [EquipmentInline]  # здесь подключаем наше табличное представление оборудования

from django.contrib import admin
from .models import Booking

from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'space', 'date', 'end_date', 'duration', 'total_price', 'confirmed', 'created_at')
    search_fields = ('user_name', 'space__name')
    list_filter = ('confirmed', 'date', 'space')
    ordering = ('-created_at',)
    list_editable = ('confirmed',)
    list_per_page = 25
    # Делаем поля, рассчитанные автоматически, только для чтения
    readonly_fields = ('duration', 'total_price', 'created_at')
    
    def get_readonly_fields(self, request, obj=None):
        # Если запись уже создана, можно также сделать "date" и "end_date" только для чтения,
        # чтобы случайно не изменить период после расчёта.
        if obj:
            return self.readonly_fields  # можно добавить ('date', 'end_date') если хотите их защитить
        return self.readonly_fields


@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_paid', 'price_per_hour')
    search_fields = ('name',)
    list_filter = ('is_paid',)
    list_per_page = 25

# Если необходимо — можно также зарегистрировать Equipment отдельно,
# но поскольку мы уже встраиваем его через Inline в Space, это бывает избыточно.
# admin.site.register(Equipment)
