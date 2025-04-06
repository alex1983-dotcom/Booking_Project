from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# === Календарь ===
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


# === Выбор месяца ===
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


# === Выбор года ===
def create_year_keyboard(prefix: str):
    """
    Создает клавиатуру для выбора года с уникальным префиксом для callback_data.
    """
    buttons = [[InlineKeyboardButton(text=str(year), callback_data=f"{prefix}_year:{year}") for year in range(2025, 2031)]]
    buttons.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# === Выбор времени: час ===
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


# === Выбор времени: минуты ===
def create_minute_keyboard(prefix: str):
    """
    Создает клавиатуру для выбора минут с уникальным префиксом для callback_data.
    """
    buttons = [
        [InlineKeyboardButton(text=f"🕒 {minute:02}", callback_data=f"{prefix}_minute:{minute}") for minute in range(0, 60, 15)]
    ]
    buttons.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# === Выбор зала ===
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_halls_keyboard(halls):
    """
    Создаёт клавиатуру для выбора залов.
    """
    buttons = [
        [InlineKeyboardButton(text=f"🏢 {hall['name']}", callback_data=f"hall:{hall['id']}")] for hall in halls
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# === Выбор количества гостей ===
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


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def create_preferences_keyboard(all_preferences):
    """
    Генерирует клавиатуру с предпочтениями в виде столбца и кнопкой завершения.
    """
    if not all_preferences or not isinstance(all_preferences, list):
        raise ValueError("Предпочтения должны быть списком объектов с ключами 'id' и 'name'.")

    buttons = [
        [InlineKeyboardButton(text=pref["name"], callback_data=f"preference:{pref['id']}")]
        for pref in all_preferences if "id" in pref and "name" in pref
    ]
    
    if not buttons:
        raise ValueError("Список предпочтений пуст или содержит некорректные данные.")

    buttons.append([InlineKeyboardButton(text="Завершить выбор", callback_data="finish_selection")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# === Контактные данные ===
def create_contact_input_keyboard():
    """
    Клавиатура для начала ввода контактных данных.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ввести контактные данные", callback_data="start_contact_input")]
    ])


# === Промокод ===
def create_promo_code_keyboard():
    """
    Клавиатура для ввода или пропуска промокода.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ввести промокод", callback_data="enter_promo_code")],
        [InlineKeyboardButton(text="Пропустить", callback_data="skip_promo_code")]
    ])


# === Мессенджеры ===
def create_messengers_keyboard():
    """
    Клавиатура для выбора мессенджеров.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Telegram", callback_data="messenger:telegram")],
        [InlineKeyboardButton(text="WhatsApp", callback_data="messenger:whatsapp")],
        [InlineKeyboardButton(text="Viber", callback_data="messenger:viber")],
        [InlineKeyboardButton(text="Пропустить", callback_data="skip_messenger")]
    ])


# === Обратная связь ===
def create_feedback_keyboard():
    """
    Создает клавиатуру для выбора обратной связи.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📞 Телефон", callback_data="feedback:phone")],
        [InlineKeyboardButton(text="💬 Мессенджер", callback_data="feedback:messenger")],
        [InlineKeyboardButton(text="🏷️ Промокод", callback_data="feedback:promo")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")],
    ])
def create_finish_contact_keyboard():
    """
    Клавиатура для завершения ввода контактных данных.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Завершить ввод данных", callback_data="contact_input")]
    ])


# === Финальные действия ===
def create_finish_keyboard():
    """
    Клавиатура для действий после завершения ввода данных.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Вернуться в меню", callback_data="main_menu")],
        [InlineKeyboardButton(text="Продолжить бронирование", callback_data="finalize_booking")],
    ])
