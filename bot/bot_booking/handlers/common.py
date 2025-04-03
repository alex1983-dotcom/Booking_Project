from aiogram import Router, types
from aiogram.fsm.context import FSMContext

router = Router()

@router.callback_query(lambda c: c.data == "cancel")
async def cancel_action(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.edit_text("Действие отменено. Выберите дальнейшее действие.")

