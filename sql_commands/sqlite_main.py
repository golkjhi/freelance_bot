import asyncio
import asyncpg
from sql_commands.sql_costumer import sql_start_company

async def sql_start():
    global cur

    cur = await asyncpg.connect('postgres://postgres:superbot134.@localhost:5432/bot_users')

    await sql_start_company()


async def check_profile(user_id):
    user = await cur.fetch(f"SELECT * FROM profile WHERE user_id = '{user_id}'")
    lst = []
    try:
        for i in user[0]:
            if i!='':
                lst.append(i)
        return True if len(lst)>2 else False
    except:
        return False


async def profile_user(user_id):
    user = await cur.fetch(f"SELECT * FROM profile WHERE user_id = '{user_id}'")
    lst = [i for i in user[0]]
    lst_user = ['id', 'name', 'age', 'country', 'language_and_experience', 'english_lvl', 'summary', 'contacts', 'photo']
    res_kwarg = {lst_user[i]: lst[i] for i in range(9)}
    return res_kwarg


async def create_profile(user_id):
    user = await cur.fetch(f"SELECT 1 FROM profile WHERE user_id = '{user_id}'")
    if not user:
        await cur.execute(f"INSERT INTO profile VALUES('{user_id}', '', '', '', '', '', '', '', '')")



async def edit_profile(state, user_id):
    async with state.proxy() as data:
        await cur.execute(f"UPDATE profile SET name = '{data['name']}', age = '{data['age']}', country = '{data['country']}',\
                    language_and_experience = '{data['language_and_experience']}', english_lvl = '{data['english_lvl']}',\
                    summary = '{data['summary']}', contacts = '{data['contacts']}', photo = '{data['photo']}' WHERE user_id = '{str(user_id)}'")


async def edit_language(state, user_id):
    async with state.proxy() as data:
        await cur.execute(f"UPDATE profile SET name = '{data['name']}', age = '{data['age']}', country = '{data['country']}',\
                    language_and_experience = '{data['language_and_experience']}', english_lvl = '{data['english_lvl']}',\
                    summary = '{data['summary']}', contacts = '{data['contacts']}', photo = '{data['photo']}' WHERE user_id = '{str(user_id)}'")


async def res_language(user_id):
    await sql_start()
    user_lang = await cur.fetch(f"SELECT user_id, language_and_experience FROM profile WHERE user_id = '{user_id}'")



async def user_for_push(language):
    await sql_start()
    lang_compane = language.strip().split()
    res_users_language = set()
    
    for ln in lang_compane:
        user = await cur.fetch(f"SELECT user_id, language_and_experience FROM profile WHERE language_and_experience LIKE '%{ln}%'")
        if user:
            for us in user:
                res_users_language.add(us[0])
    if res_users_language:
        return res_users_language

async def user_for_push_eng(end_lvl):
    await sql_start()
    eng_compane = end_lvl.strip().split()
    res_users_eng_lvl = set()
    for lvl in eng_compane:
        user_eng = await cur.fetch(f"SELECT user_id FROM profile WHERE english_lvl LIKE '%{lvl}%'")
        for i in user_eng:
            res_users_eng_lvl.add(i[0])
    return res_users_eng_lvl
    

async def result_push(lang, eng_lvl):
    if type(lang) == set and type(eng_lvl) == set:
        return lang&eng_lvl
    

async def urders_of_users(user_id):
    # await sql_start()
    user = await cur.fetch(f"SELECT customer_id, text_order FROM orders WHERE worker_id = {int(user_id)}")
    users_work = list()
    for i in user:
        id_costumer = int(i[0])
        text_customer = i[1]
        if 'a1 a2 b1 b2 c1' in text_customer.strip():
            text_customer = text_customer.strip().replace('a1 a2 b1 b2 c1', 'Не важен')
        users_work.append([id_costumer, text_customer])
    return users_work


# async def main():
#     a = await user_for_push('\n\n\n c++ hg l l')
#     print(a)
#     b = await user_for_push_eng('\n\n\n a2')
#     print(b)
#     c = await result_push(a, b)
#     print(c)
# # #     await urders_of_users(1906281245)
    

# asyncio.run(main())
