from .start_booking import router as start_router
from .process_start_day import router as start_day_router
from .process_end_day import router as end_day_router
from .process_quests_input import router as quests_input_router
from .process_hall_selection import router as hall_selection_router
from .process_preferences_selection import router as preferences_selection_router
from .finish_preferences_selection import router as finish_preferences_selection_router
from .finalize_booking import router as finalize_booking_router

# Собираем маршрутизаторы в список
routers = [
    start_router,
    start_day_router,
    end_day_router,
    quests_input_router,
    hall_selection_router,
    preferences_selection_router,
    finish_preferences_selection_router,
    finalize_booking_router,
]
