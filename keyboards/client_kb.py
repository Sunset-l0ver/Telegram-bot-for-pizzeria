from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


b1 = KeyboardButton('Режим работы')


b2 = KeyboardButton('Расположение')


b3 = KeyboardButton('Меню')


b4 = KeyboardButton('Корзина')


b5 = KeyboardButton('Очистить корзину')


b6 = KeyboardButton('Оформить')


b7 = KeyboardButton('Отмена')


button_case_client = ReplyKeyboardMarkup(resize_keyboard=True).add(
    b1).add(b2).insert(b3).add(b4).insert(b5).add(b6).insert(b7)


b_contact = KeyboardButton('Отправить номер телефона', request_contact=True)
button_contact = ReplyKeyboardMarkup(resize_keyboard=True).add(b_contact)
