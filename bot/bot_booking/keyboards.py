from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Календарь
def create_calendar(prefix: str):
    """
    Создает календарь с уникальным префиксом для callback_data.
    """
    buttons = [
        [InlineKeyboardButton(text=str(day), callback_data=f"{prefix}_day:{day}") for day in range(i, i + 7)]
        for i in range(1, 32, 7)
    ]
    buttons.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Выбор месяца
def create_month_keyboard(prefix: str):
    """
    Создает клавиатуру для выбора месяца с уникальным префиксом для callback_data.
    """
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
              'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    buttons = [
        [InlineKeyboardButton(text=month, callback_data=f"{prefix}_month:{i + 1}") for i, month in enumerate(months[j:j + 4])]
        for j in range(0, 12, 4)
    ]
    buttons.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Выбор года
def create_year_keyboard(prefix: str):
    """
    Создает клавиатуру для выбора года с уникальным префиксом для callback_data.
    """
    buttons = [[InlineKeyboardButton(text=str(year), callback_data=f"{prefix}_year:{year}") for year in range(2025, 2031)]]
    buttons.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Выбор времени: часа
def create_hour_keyboard(prefix: str):
    """
    Создает клавиатуру для выбора часа с уникальным префиксом для callback_data.
    """
    buttons = [
        [InlineKeyboardButton(text=f"⏰ {hour:02}:00", callback_data=f"{prefix}_hour:{hour}") for hour in range(i, i + 3)]
        for i in range(8, 23, 3)
    ]
    buttons.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Выбор времени: минуты
def create_minute_keyboard(prefix: str):
    """
    Создает клавиатуру для выбора минут с уникальным префиксом для callback_data.
    """
    buttons = [
        [InlineKeyboardButton(text=f"🕒 {minute:02}", callback_data=f"{prefix}_minute:{minute}") for minute in range(0, 60, 15)]
    ]
    buttons.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Выбор зала
def create_halls_keyboard(halls):
    """
    Создает клавиатуру для выбора зала.
    """
    buttons = [
        [InlineKeyboardButton(text=f"🏢 {hall['name']}", callback_data=f"hall:{hall['id']}")] for hall in halls
    ]
    buttons.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Выбор количества гостей
def create_guests_keyboard(max_guests: int, prefix: str):
    """
    Создает клавиатуру для выбора количества гостей в пределах вместимости.
    """
    buttons = [
        [InlineKeyboardButton(text=str(guests), callback_data=f"{prefix}_guests:{guests}")]
        for guests in range(1, max_guests + 1)
    ]
    buttons.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Выбор дополнительных предпочтений
def create_preferences_keyboard(preferences):
    """
    Создает клавиатуру для выбора дополнительных предпочтений из базы данных.
    """
    buttons = [
        [InlineKeyboardButton(text=f"✅ {pref['name']}", callback_data=f"preference:{pref['id']}")] for pref in preferences
    ]
    buttons.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Обратная связь
def create_feedback_keyboard():
    """
    Создает клавиатуру для выбора обратной связи.
    """
    buttons = [
        [InlineKeyboardButton(text="📞 Телефон", callback_data="feedback:phone")],
        [InlineKeyboardButton(text="💬 Мессенджер", callback_data="feedback:messenger")],
        [InlineKeyboardButton(text="🏷️ Промокод", callback_data="feedback:promo")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
