from aiogram import types, Dispatcher
from create_bot import dp, bot
from data_base.sqlite_db import *
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from handlers.admin import Send_order_to_admin
from keyboards.client_kb import button_case_client, button_contact
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMBasket(StatesGroup):
    count_req = State()


class FSMOrdering(StatesGroup):
    request_delivery_address = State()
    request_delivery_time = State()


class FSMClient_info_request(StatesGroup):
    request_name = State()
    request_contact = State()


async def cancel_client(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Заказ отменен")


async def checkout(message: types.Message):
    if await sql_view_basket(message.from_user.id) == "Корзина пуста":
        await message.answer("Ваша корзина пуста сейчас")
    else:
        await FSMOrdering.request_delivery_address.set()
        await message.answer(text="Укажите адрес доставки")


async def get_delivery_address(message: types.Message, state: FSMContext):
    await FSMOrdering.next()
    async with state.proxy() as data:
        data["userid"] = message.from_user.id
        data["place"] = message.text
    await message.answer("Укажите время доставки в формате ЧЧ:ММ (минимум 30 минут)")


async def get_delivery_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["time"] = message.text
    # * Вызов функции которая пересылает заказ админам
    await Send_order_to_admin(state)
    await sql_add_order(state, message)
    await message.answer("Спасибо. Заказ оформлен")
    await state.finish()


async def get_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["userid"] = message.from_user.id
        data["name"] = message.text
    await FSMClient_info_request.next()
    await message.answer(text="Мы запросили у вас ваш номер телефона. Пожалуйста, нажмите кнопку внизу", reply_markup=button_contact)


async def get_contact(message: types.Message, state: FSMContext):
    print("Вошел")
    async with state.proxy() as data:
        data["contact"] = message.contact.phone_number
    await sql_add_user(state)
    await state.finish()
    await message.answer(text="Благодарим! Чего желаете?", reply_markup=button_case_client)


async def command_start(message: types.Message, state: FSMContext):
    if await sql_check_user(message):
        await bot.send_message(message.from_user.id, "Вас привествует пиццерия Только вкусно! Как мы можем к вам обращаться?", reply_markup=ReplyKeyboardRemove())
        await state.finish()
        await FSMClient_info_request.request_name.set()
    else:
        state.finish
        await bot.send_message(message.from_user.id, "Вас привествует пиццерия Только вкусно!", reply_markup=button_case_client)


async def restaurant_schedule(message: types.Message):
    await bot.send_message(message.from_user.id, "Круглосуточно с 7:00 до 20:00")


async def location(message: types.Message):
    await bot.send_message(message.from_user.id, "ул. Астраханская 88")


async def empty_basket(message: types.Message):
    await sql_empty_basket(message)
    await bot.send_message(message.from_user.id, text="Корзина очищена!")

# * Дописать


async def view_basket(message: types.Message):
    if await sql_view_basket(message.from_user.id) == "Корзина пуста":
        await message.answer("Ваша корзина пуста сейчас")
    else:
        txt = await sql_view_basket(message.from_user.id)
        msg = "В вашей корзине сейчас:\n" + txt
        await bot.send_message(message.from_user.id, text=msg)


async def get_product(callback_query: types.CallbackQuery):
    await FSMBasket.count_req.set()
    state = dp.get_current().current_state()
    async with state.proxy() as data:
        data["userid"] = callback_query.from_user.id
        data["product_name"] = callback_query.data.replace(
            "add", "")
    await bot.send_message(callback_query.from_user.id, text="Введите количество")


async def get_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["count"] = int(message.text)
    await sql_add_to_basket(state)
    await message.answer(text="Позиция добавлена!")
    await state.finish()


async def menu(message: types.Message):
    read = await sql_read_menu()
    for ret in read:
        await bot.send_photo(message.from_user.id, ret[0], f"{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]} ₽", reply_markup=InlineKeyboardMarkup().
                             add(InlineKeyboardButton(f"Добавить в корзину", callback_data=f"add{ret[1]}")))


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start"])

    dp.register_message_handler(cancel_client, text="Отмена", state="*")

    dp.register_message_handler(
        restaurant_schedule, commands="restaurant_schedule")
    dp.register_message_handler(restaurant_schedule, text="Режим работы")

    dp.register_message_handler(location, commands=["location"])
    dp.register_message_handler(location, text="Расположение")

    dp.register_message_handler(menu, commands=["menu"])
    dp.register_message_handler(menu, text="Меню")

    dp.register_message_handler(view_basket, commands=["basket"])
    dp.register_message_handler(view_basket, text="Корзина")

    dp.register_message_handler(empty_basket, commands=["empty_basket"])
    dp.register_message_handler(empty_basket, text="Очистить корзину")

    dp.register_message_handler(checkout, commands=["checkout"])
    dp.register_message_handler(checkout, text="Оформить")

    dp.register_callback_query_handler(
        get_product, lambda x: x.data and x.data.startswith("add"))
    dp.register_message_handler(get_quantity, state=FSMBasket.count_req)

    dp.register_message_handler(
        get_name, state=FSMClient_info_request.request_name)

    dp.register_message_handler(
        get_contact, state=FSMClient_info_request.request_contact, content_types=["contact", ])

    dp.register_message_handler(
        get_delivery_address, state=FSMOrdering.request_delivery_address)

    dp.register_message_handler(
        get_delivery_time, state=FSMOrdering.request_delivery_time)
