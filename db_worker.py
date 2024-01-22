import sqlite3 as sq
import json
import pygame
import os


def database_maker():  # создать базу данных уровня
    con = sq.connect('NEW.db')
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS 'progress'(
        'level'   TEXT
    );
    """)
    con.commit()
    r = cur.execute("""SELECT * FROM 'progress'""").fetchall()
    if not r:
        cur.execute("""INSERT INTO 'progress'(level) VALUES(1)""")
        con.commit()
    con.close()


database_maker()


def database_changer(column, value):  # изменить базу данных
    con = sq.connect('NEW.db')
    cur = con.cursor()
    cur.execute(f"UPDATE 'progress' SET {column}=?", (value,))
    con.commit()
    con.close()


def level_determinant():  # определить уровень
    con = sq.connect('NEW.db')
    cur = con.cursor()
    r = cur.execute("""SELECT level from 'progress'""").fetchall()
    r = int(r[0][0])
    con.close()
    return r


def current_sum_determinant():
    pass


def delete_progress():  # стереть прогресс
    import os
    try:
        os.remove('progress.db')
        return True
    except FileNotFoundError:
        return False


def skin_files():  # создание файлов скинов
    if not (os.path.isfile('chosen_skin.json')):
        with open('chosen_skin.json', 'w') as json_file:
            json.dump('Sprites/general/classic_ace.png', json_file)
    if not (os.path.isfile('money.json')):
        with open('money.json', 'w') as json_file:
            json.dump(0, json_file)


skin_files()


def read_money():  # общий счёт
    with open('money.json', 'r') as json_file:
        return json.load(json_file)


def resize_screen(arg):  # изменение размера экрана
    global screen
    screen = pygame.display.set_mode(arg, pygame.NOFRAME, pygame.RESIZABLE)


def shop_db():  # созданиe базы данных скинов
    con = sq.connect('SHOP_DB.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS "shop" (
	"skin"	TEXT,
	"bought"	TEXT
);''')
    con.commit()

    r = cur.execute("""SELECT * FROM 'shop'""").fetchall()
    if not r:
        for i in range(1, 5):
            cur.execute("""INSERT INTO 'shop'(skin, bought) VALUES(?, ?)""", (i, 'no'))
            con.commit()
            i += 1
    cur.execute(f'UPDATE "shop" SET "bought"="yes" WHERE skin=?', (1,))
    con.commit()
    con.close()
    con.close()


shop_db()


def bought_skin(number):  # статус скина
    con = sq.connect('SHOP_DB.db')
    cur = con.cursor()
    r = cur.execute('SELECT bought from "shop" where skin=?', (number,)).fetchall()
    con.close()
    return r[0][0]


def buy_sk(number):  # покупка скина
    con = sq.connect('SHOP_DB.db')
    cur = con.cursor()
    cur.execute(f'UPDATE "shop" SET "bought"="yes" WHERE skin=?', (number,))
    con.commit()
    con.close()


def set_skin(skin):  # выбрать скин
    with open('chosen_skin.json', 'r') as json_file:
        json.dump(skin, json_file)


def json_checker():
    try:
        with open("chosen_skin.json", "r") as json_file:
            d = json.load(json_file)
    except Exception:
        os.remove("chosen_skin.json")
        with open('chosen_skin.json', 'w') as json_file:
            json.dump('Sprites/general/classic_ace.png', json_file)
