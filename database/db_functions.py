import sqlite3
import asyncio
def add_to_queue(user_id, card_lvl):
    con = sqlite3.connect('database/waifubot.db')
    cur = con.cursor()
    cur.execute(f"INSERT INTO queue(chat_id,card_lvl) values({user_id},{card_lvl})")
    con.commit()
    con.close()

def delete_from_queue(user_id):
    con = sqlite3.connect('database/waifubot.db')
    cur = con.cursor()
    cur.execute(f"DELETE FROM queue where chat_id = {user_id}")
    con.commit()
    con.close()

async def find_opponent(chat_id)->int:
    id = None
    con = sqlite3.connect('database/waifubot.db')
    cur = con.cursor()
    rez = None
    while rez is None:
        rez = cur.execute(f"SELECT chat_id from queue WHERE chat_id != {chat_id}").fetchone()
        id = rez
        await asyncio.sleep(1)
    return id

def create_session(my_id,opponent_id):
    con = sqlite3.connect('database/waifubot.db')
    cur = con.cursor()
    check_session = cur.execute(f'SELECT session_id FROM active_session WHERE session_id = {my_id+opponent_id}').fetchone()
    if check_session is None:
        cur.execute(f"INSERT INTO active_session values({my_id},{opponent_id},{my_id+opponent_id})")
    con.commit()
    con.close()

def get_opponent_clvl(opponent_id):
    con = sqlite3.connect('database/waifubot.db')
    cur = con.cursor()
    rez = cur.execute(f"SELECT card_lvl from queue WHERE chat_id == {opponent_id}").fetchone()
    return rez
