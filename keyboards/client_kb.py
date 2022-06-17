from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove



b1 = KeyboardButton('/restaurant_schedule')
b2 = KeyboardButton('/location')
b3 = KeyboardButton('/menu')
b4 = KeyboardButton('/view_basket')
b5 = KeyboardButton('/empty_basket')
b6 = KeyboardButton('/checkout')



button_case_client = ReplyKeyboardMarkup(resize_keyboard=True).add(b1).add(b2).insert(b3).add(b4).insert(b5).add(b6)




b_contact = KeyboardButton('Отправить номер телефона', request_contact=True)
button_contact = ReplyKeyboardMarkup(resize_keyboard=True).add(b_contact)