from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_calendar(prefix: str):
    """
    Создает календарь с уникальным префиксом для callback_data.
    Изменения: Добавлен префикс для разделения начала и конца бронирования.
    """
    buttons = [
        [InlineKeyboardButton(text=str(day), callback_data=f"{prefix}_day:{day}") for day in range(i, i + 7)]
        for i in range(1, 32, 7)
    ]
    buttons.append([InlineKeyboardButton(text="Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def create_month_keyboard(prefix: str):
    """
    Создает клавиатуру для выбора месяца с уникальным префиксом для callback_data.
    Изменения: Добавлен префикс для разделения начала и конца бронирования.
    """
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
              'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    buttons = [
        [InlineKeyboardButton(text=month, callback_data=f"{prefix}_month:{i + 1}") for i, month in enumerate(months[j:j + 4])]
        for j in range(0, 12, 4)
    ]
    buttons.append([InlineKeyboardButton(text="Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def create_year_keyboard(prefix: str):
    """
    Создает клавиатуру для выбора года с уникальным префиксом для callback_data.
    Изменения: Добавлен префикс для разделения начала и конца бронирования.
    """
    buttons = [[InlineKeyboardButton(text=str(year), callback_data=f"{prefix}_year:{year}") for year in range(2025, 2031)]]
    buttons.append([InlineKeyboardButton(text="Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def create_hour_keyboard(prefix: str):
    """
    Создает клавиатуру для выбора часа с уникальным префиксом для callback_data.
    Изменения: Добавлен префикс для разделения начала и конца бронирования.
    """
    buttons = [
        [InlineKeyboardButton(text=f"{hour:02}", callback_data=f"{prefix}_hour:{hour}") for hour in range(i, i + 3)]
        for i in range(8, 23, 3)
    ]
    buttons.append([InlineKeyboardButton(text="Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def create_minute_keyboard(prefix: str):
    """
    Создает клавиатуру для выбора минут с уникальным префиксом для callback_data.
    Изменения: Добавлен префикс для разделения начала и конца бронирования.
    """
    buttons = [
        [InlineKeyboardButton(text=f"{minute:02}", callback_data=f"{prefix}_minute:{minute}") for minute in range(0, 60, 15)]
    ]
    buttons.append([InlineKeyboardButton(text="Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def create_halls_keyboard(halls):
    # Ожидаем, что halls является списком объектов
    buttons = [
        [InlineKeyboardButton(text=hall['name'], callback_data=f"hall:{hall['id']}")] for hall in halls
    ]
    buttons.append([InlineKeyboardButton(text="Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
