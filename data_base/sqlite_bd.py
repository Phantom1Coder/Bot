import sqlite3 as sq
from aiogram import types
import datetime

def sql_start():
    global base, cur
    base = sq.connect("users.bd")
    cur = base.cursor()
    if base:
        print("Secusefull connect to BD")
        base.execute('''CREATE TABLE IF NOT EXISTS users ( status TEXT, username TEXT, telegram_id INTEGER, date_reg TEXT )''')
        base.commit()
sql_start()

def add_user(username, telegram_id, date_reg):
    date_reg = datetime.datetime.today().strftime("%Y-%m-%d")
    cur.execute("INSERT INTO users (status, username, telegram_id, date_reg) VALUES (?, ?, ?, ?)", ('1', username, telegram_id, date_reg))
    base.commit()

def is_user_in_db(telegram_id):
    cur.execute("SELECT * FROM users WHERE telegram_id=?", (telegram_id,))
    user = cur.fetchone()
    return user

def get_user_id_by_username(username):
    cur.execute("SELECT telegram_id FROM users WHERE username=?", (username,))
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        return None

def get_user_info(telegram_id):
    try:
        conn = sq.connect("users.bd")  # Подставьте имя вашей базы данных
        cursor = conn.cursor()
        cursor.execute("SELECT date_reg, telegram_id, username, status FROM users WHERE telegram_id=?", (telegram_id,))
        user_info = cursor.fetchone()
        return user_info  # Возвращает кортеж с информацией о пользователе (reg_data, telegram_id, username, status)
    except sq.Error as e:
        print("Ошибка при получении информации о пользователе:", e)
        return None
    finally:
        if conn:
            conn.close()