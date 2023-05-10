import json
import sqlite3
import asyncio
from io import StringIO
from PIL import Image
import numpy as np
import base64


def convert_to_binary(file):
    fin = open(file, "rb")
    img = fin.read()
    return img
    fin.close()


class Database:
    con = sqlite3.connect('database/waifubot.db')
    cur = con.cursor()
    @classmethod
    def add_to_queue(cls, user_id, card_lvl):
        cls.cur.execute(f"INSERT INTO queue(chat_id,card_lvl) values({user_id},{card_lvl})")
        cls.con.commit()
        print('DOLBIT')
    @classmethod
    def delete_from_queue(cls,user_id):
        cls.cur.execute(f"DELETE FROM queue where chat_id = {user_id}")
        cls.con.commit()
    @classmethod
    async def find_opponent(cls,chat_id)->int:
        id = None
        rez = None
        while rez is None:
            rez = cls.cur.execute(f"SELECT chat_id from queue WHERE chat_id != {chat_id}").fetchone()
            id = rez
            await asyncio.sleep(1)
        return id
    @classmethod
    def create_session(cls, my_id,opponent_id):
        check_session = cls.cur.execute(f'SELECT session_id FROM active_session WHERE session_id = {my_id+opponent_id}').fetchone()
        if check_session is None:
            cls.cur.execute(f"INSERT INTO active_session values({my_id},{opponent_id},{my_id+opponent_id})")
        cls.con.commit()
    @classmethod
    def get_opponent_clvl(cls,opponent_id):
        rez = cls.cur.execute(f"SELECT card_lvl from queue WHERE chat_id == {opponent_id}").fetchone()
        return rez

    @classmethod
    def get_user_cards(cls,user_id):
        rez = cls.cur.execute(f"SELECT card_ids FROM user_cards WHERE user_id == {user_id}")
        rez = rez.fetchall()
        if len(rez) > 0:
            print(rez)
            rez = rez[0][0].split(';')
            rez_json = [json.loads(i) for i in rez]
            return rez_json

    @classmethod
    def upload_photo(cls,file):
        blob = convert_to_binary(file)
        blob = sqlite3.Binary(blob)
        print(blob)
        cls.cur.execute(f"INSERT INTO cards(photo_lvl1) VALUES (?)", (blob,))
        cls.con.commit()

    @classmethod
    def take_photo(cls,id,lvl):
        res = cls.cur.execute(f"SELECT photo_lvl{lvl} FROM cards WHERE id == {id}")
        res = res.fetchone()[0]
        return res






