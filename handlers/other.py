from aiogram import types, Dispatcher





async def defunct_command(message: types.Message):
    await message.answer(text="Несуществующая команда")
    await message.delete()






def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(defunct_command)