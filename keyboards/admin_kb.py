from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button_load = KeyboardButton("/загрузить")
button_delete = KeyboardButton("/удалить")
button_cancel = KeyboardButton("/отмена")


button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load).add(button_delete).add(button_cancel)