import asyncio
import asyncpg
from config import DATABASE

async def sql_start_company():
    global cur

    cur = await asyncpg.connect(DATABASE)


async def create_profile_company(customer_id):
    user = await cur.fetch(f"SELECT 1 FROM profile_costumer WHERE customer_id = '{customer_id}'")
    if not user:
        await cur.execute(f"INSERT INTO profile_costumer VALUES('{customer_id}', '', '', '', 0)")


async def profile_company(customer_id):
    await sql_start_company()
    user = await cur.fetch(f"SELECT * FROM profile_costumer WHERE customer_id = '{customer_id}'")
    if user:
        lst = [i for i in user[0]]
        return False if '' in lst else lst
    else:
        return False
    

async def tasks_company(customer_id):
    # await sql_start_company()
    user = await cur.fetch(f"SELECT order_id, customer_id, text_order FROM orders WHERE customer_id = '{customer_id}'")
    lst = [i for i in user]
    for i in range(len(lst)):
        lst[i] = [lst[i][0], lst[i][1], lst[i][2]]
    return lst


async def del_task(order_id):
    # await sql_start_company()
    await cur.fetch(f"DELETE FROM orders WHERE order_id = '{order_id}'")
    print('Запрос передан')


async def edit_company_profile(state, customer_id):
    async with state.proxy() as data:
        await cur.execute(f"UPDATE profile_costumer SET name_company = '{data['name_company']}', about_company = '{data['about_company']}',\
                    links = '{data['links']}' WHERE customer_id = '{str(customer_id)}'")
        

async def add_order(customer_id, lst_users, text):
    # await sql_start_company()
    for i in lst_users:
        await cur.execute(f"INSERT INTO orders (worker_id, customer_id, text_order) VALUES({int(i)}, {int(customer_id)}, '{text}')")
        


# asyncio.run(del_task(123))

