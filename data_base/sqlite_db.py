from email.message import Message
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
    base.execute("CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price integer)")
    base.execute("CREATE TABLE IF NOT EXISTS basket(userID integer, product_name, count integer)")
    base.execute("CREATE TABLE IF NOT EXISTS users(userID integer, username text, phone_number text)")
    base.execute("CREATE TABLE IF NOT EXISTS orders(orderID integer, userID integer, ordering_content, delivery_place, delivery_time)")
    base.commit()





async def sql_add(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO menu VALUES (?, ?, ?, ?)", tuple(data.values()))
        base.commit()





async def sql_read_admin(message):
    for ret in cur.execute("SELECT * FROM menu").fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f"{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}")





async def sql_read2():
    return cur.execute("SELECT * FROM menu").fetchall()





async def sql_delete(data):
    cur.execute("DELETE FROM menu WHERE name == ?", (data,))
    base.commit()





async def sql_add_to_basket(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO basket VALUES (?, ?, ?)", tuple(data.values()))
        base.commit()





async def sql_empty_basket(message: types.Message):
    cur.execute("DELETE FROM basket WHERE userid == ?", (message.from_user.id,))
    base.commit()
    await bot.send_message(message.from_user.id, text="Корзина очищена!")





async def sql_view_basket(message: types.Message):
    read = cur.execute("SELECT * FROM basket WHERE userid == ?", (message.from_user.id,)).fetchall()
    msg = "В вашей корзине сейчас:\n"
    total_sum = 0
    for entry in read:
        price = cur.execute("SELECT price FROM menu WHERE name == ?", (entry[1],)).fetchone()[0]
        total_sum += price * entry[2]
        msg += entry[1] + " " + str(entry[2]) + " шт" + "\n"
    msg += f"Итоговая сумма {total_sum}"
    await bot.send_message(message.from_user.id, text = msg)





async def sql_add_user(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO users VALUES(?,?)", tuple(data["name"], data["contact"]))
        base.commit





async def sql_check_user(message: types.Message):
    return cur.execute("SELECT * FROM users WHERE userid == ?", (message.from_user.id,)).fetchone() is None





async def sql_add_user(state: FSMContext):
    async with state.proxy() as data:
        cur.execute("INSERT INTO users VALUES(?, ?, ?)", (data["userid"], data["name"], data["contact"]))
    base.commit()





async def sql_add_order(state: FSMContext, message: types.Message):
    async with state.proxy() as data:
        basket_contents = cur.execute("SELECT * FROM basket WHERE userid == ?", (data["userid"],)).fetchall()
        # ! CREATE TABLE IF NOT EXISTS orders(orderID integer, userID integer, ordering_content, delivery_place, delivery_time)
        basket = ""
        for pos in basket_contents:
            basket += pos[1] + " " + str(pos[2]) + "\n"
        last_id = cur.execute("SELECT MAX(orderid) FROM orders").fetchone()[0]
        if last_id == None:
            last_id = 1
        cur.execute("INSERT INTO orders VALUES(?, ?, ?, ?, ?)", (last_id, data["userid"], basket, data["place"], data["time"],))
        base.commit()
    await sql_empty_basket(message)