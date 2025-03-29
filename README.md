# Документация по моделям

### 1. **Модуль `space_models.py`**

#### 1.1. **Абстрактная модель `AbstractItem`**

```python
class AbstractItem(models.Model):
    """
    Общие свойства для моделей помещений и доп. опций.
    """
    name = models.CharField(max_length=20, default='test_name',
                            help_text='Название', verbose_name='Название')  # Название
    description = models.TextField(default='test_description',
                                   help_text='Описание', verbose_name='Описание') # Описание

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return f'{self.name}: {self.description[:20]}...'
```

- **Назначение**: Абстрактная модель, которая определяет общие поля для моделей, связанных с помещениями и дополнительными опциями.
- **Поля**:
  - `name`: Название объекта (макс. 20 символов).
  - `description`: Описание объекта.
- **Meta**:
  - `abstract = True`: Модель не будет создана в базе данных.
  - `ordering = ['name']`: Указывает порядок сортировки объектов по имени.
- **Метод `__str__`**: Возвращает строковое представление объекта.

#### 1.2. **Модель `Space`**

```python
class Space(AbstractItem):
    """
    Модель, представляющая пространство для бронирования.
    """
    capacity = models.PositiveIntegerField(default=1)  # Вместимость пространства
    area = models.PositiveIntegerField(default=1) # Площадь в метрах квадратных

    class Meta:
        verbose_name = "Пространство"
        verbose_name_plural = "Пространства"
```

- **Назначение**: Модель, представляющая пространство, которое можно забронировать.
- **Поля**:
  - `capacity`: Вместимость пространства (положительное целое число).
  - `area`: Площадь пространства в квадратных метрах (положительное целое число).
- **Meta**: Задает человекочитаемые имена для модели.

#### 1.3. **Модель `Option`**

```python
class Option(AbstractItem):
    all_count = models.PositiveIntegerField(default=1, help_text='Количество', verbose_name='Количество')

    class Meta:
        verbose_name = 'Дополнительная опция'
        verbose_name_plural = 'Дополнительные опции'
```

- **Назначение**: Модель, представляющая дополнительные опции для бронирования.
- **Поля**:
  - `all_count`: Количество доступных опций.
- **Meta**: Задает человекочитаемые имена для модели.

### 2. **Модуль `booking_models.py`**

#### 2.1. **Модель `Booking`**

```python
class Booking(models.Model):
    """
    Модель, представляющая бронирование.
    """
    space = models.ForeignKey('Space', on_delete=models.CASCADE)  # Связь с пространством
    event_start_date = models.DateTimeField(default=datetime.datetime.now)  # Дата и время начала бронирования
    event_end_date = models.DateTimeField()  # Дата и время окончания бронирования
    event_format = models.CharField(max_length=100)  # Формат мероприятия
    guests_count = models.PositiveIntegerField()  # Количество гостей
    preferences = models.JSONField()  # Дополнительные предпочтения
    promo_code = models.CharField(max_length=50, blank=True, null=True)  # Промокод (опционально)
    contact_method = models.CharField(max_length=50)  # Контактные данные
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания записи

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['event_start_date']

    def __str__(self):
        return f"Бронирование {self.space.name} с {self.event_start_date} по {self.event_end_date}"
```

- **Назначение**: Модель, представляющая запись о бронировании пространства.
- **Поля**:
  - `space`: Связь с моделью `Space` (один ко многим).
  - `event_start_date`: Дата и время начала бронирования.
  - `event_end_date`: Дата и время окончания бронирования.
  - `event_format`: Формат мероприятия.
  - `guests_count`: Количество гостей.
  - `preferences`: Дополнительные предпочтения в формате JSON.
  - `promo_code`: Промокод (необязательное поле).
  - `contact_method`: Контактные данные.
  - `created_at`: Дата и время создания записи.
- **Meta**: Задает порядок сортировки по дате начала события.

### 3. **Модуль `price_models.py`**

#### 3.1. **Абстрактная модель `PriceAbstract`**

```python
class PriceAbstract(models.Model):
    date_new_price = models.DateField(default=datetime.datetime.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.price} руб/час с {self.date_new_price}'
```

- **Назначение**: Абстрактная модель для хранения цен.
- **Поля**:
  - `date_new_price`: Дата, когда была установлена новая цена.
  - `price`: Цена (десятичное число с двумя знаками после запятой).
- **Meta**: Модель не будет создана в базе данных.

#### 3.2. **Модель `PriceSpace`**

```python
class PriceSpace(PriceAbstract):
    space_id = models.ForeignKey(to='Space', on_delete=models.CASCADE,
                                 related_name='price_of_space')

    class Meta:
        verbose_name = "Цены на помещения"
```

- **Назначение**: Модель для хранения цен на пространства.
- **Поля**:
  - `space_id`: Связь с моделью `Space`.
- **Meta**: Задает человекочитаемое имя для модели.

#### 3.3. **Модель `PriceOption`**

```python
class PriceOption(PriceAbstract):
    option_id = models.ForeignKey(to='Option', on_delete=models.CASCADE,
                                  related_name='price_of_option')

    class Meta:
        verbose_name = 'Цены на дополнительные услуги'
```

- **Назначение**: Модель для хранения цен на дополнительные опции.
- **Поля**:
  - `option_id`: Связь с моделью `Option`.
- **Meta**: Задает человекочитаемое имя для модели.

### Общая структура и взаимодействие

1. **Абстрактные модели** (`AbstractItem`, `PriceAbstract`):
   - Позволяют избежать дублирования кода, определяя общие поля и поведение для других моделей.

2. **Основные модели**:
   - `Space` и `Option` используют `AbstractItem` для описания пространств и дополнительных опций.
   - `Booking` связывает бронирования с пространствами и содержит информацию о мероприятиях.
   - `PriceSpace` и `PriceOption` определяют цены для соответствующих моделей.

3. **Связи**:
   - Используются связи один ко многим (`ForeignKey`), чтобы связать бронирования с пространствами и цены с опциями и пространствами.

