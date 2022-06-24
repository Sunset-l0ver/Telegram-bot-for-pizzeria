from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot
from aiogram import types, Dispatcher
from data_base import sqlite_db 
from keyboards import admin_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup





class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()





AdminID = set()





async def admin_load(message : types.Message):
    global AdminID
    if message.from_user.id in AdminID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')





async def cancel_handler(message : types.Message, state : FSMContext):
    current_state = state.get_state
    if current_state is None:
        return
    await state.finish()
    await message.reply("OK")





async def load_photo(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply("Теперь введи название")





async def load_name(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.reply("Введи описание")





async def load_description(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.reply("Отлично! Укажи цену")





async def load_price(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = int(message.text)
    await sqlite_db.sql_add(state)
    await message.answer(text="Позиция добавлена!")
    await state.finish()





async def make_changes(message : types.Message):
    global AdminID
    AdminID.add(message.from_user.id)
    await bot.send_message(message.from_user.id, "Что прикажете хозяин???", reply_markup=admin_kb.button_case_admin)
    await message.delete()





async def del_callback(callback_query : types.CallbackQuery):
    await sqlite_db.sql_delete(callback_query.data.replace("del ", ""))
    await callback_query.answer(text=f"{callback_query.data.replace('del ', '')} удалена.", show_alert=True)





async def delete_item(message: types.Message):
    global AdminID
    if message.from_user.id in AdminID:
        read = await sqlite_db.sql_read_menu()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f"{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}")
            await bot.send_message(message.from_user.id, text= "^^^^", reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f"удалить {ret[1]}", callback_data=f"del {ret[1]}")))





def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_load, commands='загрузить', state = None)
    
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    
    dp.register_message_handler(load_photo, content_types=["photo"], state=FSMAdmin.photo)
    
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    
    dp.register_message_handler(make_changes, commands="moderator", is_chat_admin = True)
    
    dp.register_callback_query_handler(del_callback, lambda x: x.data and x.data.startswith("del "))
    
    dp.register_message_handler(delete_item, commands="удалить")