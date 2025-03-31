# Документация по моделям
---

### `__init__.py`
Этот файл служит для создания пакета из директории, в которой он находится. Он импортирует классы моделей из других модулей, таких как `space_models`, `booking_models` и `price_models`.

Импортируемые модули:
- `AbstractItem`, `Space`, `Option` из `space_models`.
- `Booking` из `booking_models`.
- `PriceAbstract`, `PriceSpace`, `PriceOption` из `price_models`.

---

### `booking_models.py`

#### **Preference**
- **Описание:** Представляет предпочтения, которые могут быть указаны в бронировании.
- **Поля:**
  - `name` (`CharField`): Название предпочтения, строка длиной до 50 символов.
- **Методы:**
  - `__str__`: Возвращает название предпочтения.

---

#### **Booking**
- **Описание:** Модель для представления бронирования.
- **Поля:**
  - `space` (`ForeignKey`): Ссылка на модель `Space`, представляет бронируемое пространство.
  - `event_start_date` (`DateTimeField`): Дата и время начала бронирования.
  - `event_end_date` (`DateTimeField`): Дата и время окончания бронирования.
  - `event_format` (`CharField`): Формат мероприятия, строка до 100 символов.
  - `guests_count` (`PositiveIntegerField`): Количество гостей.
  - `preferences` (`ManyToManyField`): Ссылка на модель `Preference`, дополнительные пожелания.
  - `promo_code` (`CharField`): Промокод для скидки (необязательное поле).
  - `contact_method` (`CharField`): Способ связи, строка длиной до 50 символов.
  - `created_at` (`DateTimeField`): Дата и время создания бронирования.
  - `status` (`IntegerField`): Текущий статус бронирования. Возможные значения:
    - 1: Свободно.
    - 2: Забронировано.
- **Методы:**
  - `__str__`: Возвращает строковое представление бронирования.
  - `get_status_display`: Возвращает текстовый статус в зависимости от значения поля `status`.
- **Метаданные:**
  - `verbose_name`: "Бронирование".
  - `verbose_name_plural`: "Бронирования".
  - `ordering`: Сортировка по `event_start_date`.

---

### `space_models.py`

#### **AbstractItem**
- **Описание:** Абстрактный класс для общих характеристик.
- **Поля:**
  - `name` (`CharField`): Название.
  - `description` (`TextField`): Описание.
- **Метаданные:**
  - `abstract`: Класс абстрактный.
  - `ordering`: Сортировка по полю `name`.
- **Методы:**
  - `__str__`: Возвращает строку вида "name: первые 20 символов description".

---

#### **Space**
- **Описание:** Представляет пространство для бронирования.
- **Наследуется от:** `AbstractItem`.
- **Поля:**
  - `capacity` (`PositiveIntegerField`): Вместимость пространства.
  - `area` (`PositiveIntegerField`): Площадь в квадратных метрах.
- **Метаданные:**
  - `verbose_name`: "Пространство".
  - `verbose_name_plural`: "Пространства".

---

#### **Option**
- **Описание:** Дополнительные опции для бронирования.
- **Наследуется от:** `AbstractItem`.
- **Поля:**
  - `all_count` (`PositiveIntegerField`): Общее количество.
- **Метаданные:**
  - `verbose_name`: "Дополнительная опция".
  - `verbose_name_plural`: "Дополнительные опции".

---

### `price_models.py`

#### **AbstractItem**
- **Описание:** Абстрактная модель с общими свойствами (аналогичная `AbstractItem` в `space_models.py`).

#### **Space**
- **Описание:** Модель для пространств (аналогичная `Space` в `space_models.py`).

#### **Option**
- **Описание:** Дополнительные опции (аналогичная `Option` в `space_models.py`).


# Настройка административного сайта
---

### **Административный интерфейс**

#### **SpaceAdmin**
- **Описание:** Конфигурация админки для модели `Space`.
- **Настройки:**
  - `list_display`: Отображает поля `id`, `name`, `capacity`, `area` в таблице админки.
  - `search_fields`: Добавляет поле `name` для поиска.
  - `list_filter`: Фильтры по полям `capacity` и `area`.

---

#### **OptionAdmin**
- **Описание:** Конфигурация админки для модели `Option`.
- **Настройки:**
  - `list_display`: Отображает поля `id`, `name`, `all_count` в таблице админки.
  - `search_fields`: Добавляет поле `name` для поиска.
  - `list_filter`: Фильтр по полю `all_count`.

---

#### **PreferenceAdmin**
- **Описание:** Конфигурация админки для модели `Preference`.
- **Настройки:**
  - `list_display`: Отображает поля `id`, `name` в таблице админки.
  - `search_fields`: Добавляет поле `name` для поиска.

---

#### **BookingAdmin**
- **Описание:** Конфигурация админки для модели `Booking`.
- **Настройки:**
  - `form`: Используется пользовательская форма `BookingForm`.
  - `list_display`: Отображает поля `id`, `space`, `event_start_date`, `event_end_date`, `guests_count`, `status`.
  - `search_fields`: Поля `space__name` и `event_format` доступны для поиска.
  - `list_filter`: Фильтры по полям `event_start_date` и `status`.
  - `filter_horizontal`: Добавляет интерфейс для удобного выбора поля `preferences`.

---

#### **PriceSpaceAdmin**
- **Описание:** Конфигурация админки для модели `PriceSpace`.
- **Настройки:**
  - `list_display`: Отображает поля `id`, `space_id`, `price`, `date_new_price`.
  - `search_fields`: Поле `space_id__name` для поиска.
  - `list_filter`: Фильтр по полю `date_new_price`.

---

#### **PriceOptionAdmin**
- **Описание:** Конфигурация админки для модели `PriceOption`.
- **Настройки:**
  - `list_display`: Отображает поля `id`, `option_id`, `price`, `date_new_price`.
  - `search_fields`: Поле `option_id__name` для поиска.
  - `list_filter`: Фильтр по полю `date_new_price`.

---

#### **BookingForm**
- **Описание:** Пользовательская форма для модели `Booking`.
- **Настройки:**
  - `model`: Указывает, что форма создаётся для модели `Booking`.
  - `fields`: Указывает, что в форме должны быть все поля модели (`'__all__'`).


#  Схема моделей

    +-----------------+           +-----------------+
    |   AbstractItem  |           |  Preference     |
    |-----------------|           |-----------------|
    | - name          |<------┐   | - name          |
    | - description   |       |   +-----------------+
    +-----------------+       |         ▲
                              |         |
                              |      +-----------------+
    +-----------------+       |----->|    Booking      |
    |     Space       |              |-----------------|
    |-----------------|              | - space (FK)    |
    | -number_of_seats|              | - event_start   |
    | - area
    | -           |              | - event_end     |
    |-----------------|              | - event_format  |
    | Inherits:       |              | - guests_count  |
    | AbstractItem    |              | - preferences   |
    +-----------------+              | - promo_code    |
                                     | - contact_method|
                                     | - status        |
    +-----------------+              +-----------------+
    |     Option      |
    |-----------------|
    | - all_count     |
    |-----------------|
    | Inherits:       |
    | AbstractItem    |
    +-----------------+

    +-----------------+           +-----------------+
    |     PriceSpace  |           |   PriceOption   |
    |-----------------|           |-----------------|
    | - space_id      |           | - option_id     |
    | - price         |           | - price         |
    | - date_new_price|           | - date_new_price|
    +-----------------+           +-----------------+

