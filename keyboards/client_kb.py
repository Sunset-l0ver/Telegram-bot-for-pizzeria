from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove



# TODO b1 = KeyboardButton('/restaurant_schedule')
b1 = KeyboardButton('Режим работы')

# TODO b2 = KeyboardButton('/location')
b2 = KeyboardButton('Расположение')

# TODO b3 = KeyboardButton('/menu')
b3 = KeyboardButton('Меню')

# TODO b4 = KeyboardButton('/view_basket')
b4 = KeyboardButton('Корзина')

# TODO b5 = KeyboardButton('/empty_basket')
b5 = KeyboardButton('Очистить корзину')

# TODO b6 = KeyboardButton('/checkout')
b6 = KeyboardButton('Оформить')

b7 = KeyboardButton('Отмена')



button_case_client = ReplyKeyboardMarkup(resize_keyboard=True).add(b1).add(b2).insert(b3).add(b4).insert(b5).add(b6).insert(b7)




b_contact = KeyboardButton('Отправить номер телефона', request_contact=True)
button_contact = ReplyKeyboardMarkup(resize_keyboard=True).add(b_contact)