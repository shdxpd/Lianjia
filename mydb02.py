# -*- coding: utf-8 -*-
import sqlite3

def create_db():
    conn = sqlite3.connect('URL.db')
    cu = conn.cursor()
    print("Create_db success")

def create_table():
    conn = sqlite3.connect('URL.db')
    cu = conn.cursor()
    cu.execute('''CREATE TABLE IF NOT EXISTS 'url_total' (
        'urls' PRIMARY KEY,
        'ershoufang'
        )''')
    print("Create_table url_total success")
    conn.commit()

def update_table(datas):
#    print('Update_table OR IGNORE for',data)
    save_sql = 'INSERT OR IGNORE INTO url_total values (?, ?)'
    conn = sqlite3.connect('URL.db')
    cu = conn.cursor()
    for data in datas:
        cu.execute(save_sql,data)
    conn.commit()

def get_data():
    conn = sqlite3.connect('URL.db')
    cu = conn.cursor()
    cu.execute('select * from url_total')
    pages = cu.fetchall()
    conn.close()
    return pages

def close_table():
    conn = sqlite3.connect('URL.db')
    conn.close()