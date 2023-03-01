from create_bot import dp
from aiogram import executor
from sql_commands.sqlite_main import *
from handlers import client, company, other, parsing_


async def on_startapp(_):
    await sql_start()
    print('База данных создана')

other.register_handlers_other(dp)
company.register_handlers_company(dp)
client.register_handlers_client(dp)
parsing_.register_handlers_parsing(dp)


    
if __name__ == '__main__':
    executor.start_polling(dp,
                           on_startup=on_startapp,
                           skip_updates=True,
                            )