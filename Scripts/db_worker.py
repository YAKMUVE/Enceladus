import sqlite3 as sq

def database_maker():
    con = sq.connect('NEW.db')
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS 'achievements'(
        'level'   TEXT,
        'sum' INTEGER,
        'weapon'  TEXT,
        'extra'   TEXT
    );
    """)
    con.commit()
    r = cur.execute("""SELECT * FROM 'achievements'""").fetchall()
    if not r:
        cur.execute("""INSERT INTO 'achievements'(level) VALUES('0')""")
        con.commit()
    con.close()


def database_changer(column, value):
    con = sq.connect('NEW.db')
    cur = con.cursor()
    cur.execute(f"UPDATE 'achievements' SET {column}=?", (value,))
    con.commit()
    con.close()


def level_determinant():
    con = sq.connect('NEW.db')
    cur = con.cursor()
    r = cur.execute("""SELECT level from 'achievements'""").fetchall()
    r = int(r[0][0])
    con.close()
    return r

def cur_lvl_db(cur_lvl):
    pass