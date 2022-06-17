from aiogram.utils import executor
from create_bot import *
from data_base.sqlite_db import sql_start
from handlers import client, admin



async def on_startup(_):
    print("Бот в сети")
    sql_start()



client.register_handlers_client(dp)
admin.register_handlers_admin(dp)



executor.start_polling(dp, skip_updates=True, on_startup=on_startup)