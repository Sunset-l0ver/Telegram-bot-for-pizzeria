import sqlite3 as sq
from create_bot import bot
from aiogram import types
from aiogram.dispatcher import FSMContext


def sql_start():
    global base, cur
    base = sq.connect("only_tasty.db")
    cur = base.cursor()
    if base:
        print("База данных подключена успешно!")
    base.execute(
        "CREATE TABLE IF NOT EXISTS МЕНЮ(Изображение TEXT, Наименование_товара TEXT PRIMARY KEY, Описание TEXT, Цена integer)")
    base.execute(
        "CREATE TABLE IF NOT EXISTS КОРЗИНА(ID_пользователя TEXT, Наименование_товара, Количество integer)")
    base.execute(
        "CREATE TABLE IF NOT EXISTS ПОЛЬЗОВАТЕЛИ(ID_пользователя TEXT, Имя_пользователя TEXT, Номер_телефона TEXT)")
    base.execute("CREATE TABLE IF NOT EXISTS ЗАКАЗЫ(ID_заказа integer, ID_пользователя TEXT, Содержание_заказа, Место_доставки, Время_доставки, Статус INTEGER)")
    base.execute(
        "CREATE TABLE IF NOT EXISTS АДМИНИСТРАТОРЫ(ID_пользователя TEXT)")
    base.commit()


async def sql_add(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO МЕНЮ VALUES (?, ?, ?, ?)",
                    tuple(data.values()))
        base.commit()


# async def sql_read_admin(message):
#     for ret in cur.execute("SELECT * FROM menu").fetchall():
#         await bot.send_photo(message.from_user.id, ret[0], f"{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}")


async def sql_read_menu():
    return cur.execute("SELECT * FROM МЕНЮ").fetchall()


async def sql_delete(data):
    cur.execute("DELETE FROM МЕНЮ WHERE Наименование_товара == ?", (data,))
    base.commit()


async def sql_add_to_basket(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO КОРЗИНА VALUES (?, ?, ?)",
                    tuple(data.values()))
        base.commit()


async def sql_empty_basket(message: types.Message):
    cur.execute("DELETE FROM КОРЗИНА WHERE ID_пользователя == ?",
                (message.from_user.id,))
    base.commit()


async def sql_view_basket(id):
    read = cur.execute("SELECT * FROM КОРЗИНА WHERE ID_пользователя == ?",
                       (id,)).fetchall()
    ret = ""
    total_sum = 0
    for entry in read:
        price = cur.execute(
            "SELECT Цена FROM МЕНЮ WHERE Наименование_товара == ?", (entry[1],)).fetchone()[0]
        total_sum += price * entry[2]
        ret += entry[1] + " " + str(entry[2]) + " шт" + "\n"
    ret += f"Итоговая сумма {total_sum}"
    return ret


async def sql_add_user(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO ПОЛЬЗОВАТЕЛИ VALUES(?,?)",
                    tuple(data["name"], data["contact"]))
        base.commit


async def sql_check_user(message: types.Message):
    return cur.execute("SELECT * FROM ПОЛЬЗОВАТЕЛИ WHERE ID_пользователя == ?", (message.from_user.id,)).fetchone() is None


async def sql_add_user(state: FSMContext):
    async with state.proxy() as data:
        cur.execute("INSERT INTO ПОЛЬЗОВАТЕЛИ VALUES(?, ?, ?)",
                    (data["userid"], data["name"], data["contact"]))
    base.commit()


async def sql_add_order(state: FSMContext, message: types.Message):
    async with state.proxy() as data:
        basket_contents = cur.execute(
            "SELECT * FROM КОРЗИНА WHERE ID_пользователя == ?", (data["userid"],)).fetchall()
        basket = ""
        for pos in basket_contents:
            basket += pos[1] + " " + str(pos[2]) + "\n"
        last_id = cur.execute(
            "SELECT MAX(ID_заказа) FROM ЗАКАЗЫ").fetchone()[0]
        if last_id == None:
            last_id = 1
        cur.execute("INSERT INTO ЗАКАЗЫ VALUES(?, ?, ?, ?, ?, ?)",
                    (last_id, data["userid"], basket, data["place"], data["time"], 0))
        base.commit()
    await sql_empty_basket(message)


async def sql_add_admin(message: types.Message):
    if cur.execute("SELECT * FROM АДМИНИСТРАТОРЫ WHERE ID_пользователя == ?", (message.from_user.id,)).fetchone() is None:
        cur.execute("INSERT INTO АДМИНИСТРАТОРЫ VALUES(?)", (message.from_user.id,))
    base.commit()


# TODO добавить функцию для забора заказа
async def sql_get_order():
    last_id = cur.execute("SELECT MAX(ID_заказа) FROM ЗАКАЗЫ").fetchone()[0]
    order = cur.execute(
        "SELECT * FROM ЗАКАЗЫ WHERE ID_заказа == ?", (last_id,))
    msg = ""
    for pos in order:
        msg += pos + "\n"


async def sql_is_admin(id):
    return not(cur.execute("SELECT * FROM АДМИНИСТРАТОРЫ WHERE ID_пользователя == ?", (id,)).fetchone() is None)


async def sql_get_admins():
    return cur.execute("SELECT * FROM АДМИНИСТРАТОРЫ").fetchall()