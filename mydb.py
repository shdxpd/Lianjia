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
    cu.execute('''CREATE TABLE 'table_1225' (
        ‘House_id’ PRIMARY KEY,
        'TotalPrice',
        'UnitPrice',
        'house_old',
        'house_size',
        'house_address'
        )''')
    print("Create_table table_1228 success")
    conn.commit()
    conn.close()

def update_table(data):
    print('Update_table for',data)
    save_sql = 'INSERT INTO table_1225 values (?, ?, ?, ?, ?, ?)'
    conn = sqlite3.connect('Lianjia.db')
    cu = conn.cursor()
    cu.execute(save_sql,data)
    conn.commit()
    conn.close()
