# -*- coding: utf-8 -*-
import sqlite3

def create_db():
    conn = sqlite3.connect('Lianjia.db')
    cu = conn.cursor()
    conn.close()
    print("Create_db success")

def create_table():
    conn = sqlite3.connect('Lianjia.db')
    cu = conn.cursor()
    cu.execute('''CREATE TABLE IF NOT EXISTS 'table_0103' (
        'House_URL' PRIMARY KEY,
        'TotalPrice',
        'UnitPrice',
        'house_old',
        'house_size',
        'house_address'
        )''')
    print("Create_table table_0103 success")
    conn.commit()
    conn.close()

def update_table(datas):
#    print('Update_table OR IGNORE for',data)
    save_sql = 'INSERT OR IGNORE INTO table_0103 values (?, ?, ?, ?, ?, ?)'
    conn = sqlite3.connect('Lianjia.db')
    cu = conn.cursor()
    for data in datas:
        cu.execute(save_sql,data)
    conn.commit()
    conn.close()
