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
    cu.execute('''CREATE TABLE 'table_1224' (
        ‘House_id’ PRIMARY KEY,
        'TotalPrice(总价/万)',
        'UnitPrice(单价/元每平)',
        'Rom_mainInfo(户型)',
        'Rom_subInfo(楼层)',
        'Area_mainInfo(面积)',
        'Area_subInfo(房龄)',
        'label(小区名)',
        'HouseUrl'
        )''')
    print("Create_table table_1224 success")
    conn.commit()
    conn.close()

def update_table(data):
    print('Update_table for',data)
    save_sql = 'INSERT INTO table_1224 values (?, ?, ?, ?, ?, ?, ?, ?, ?)'
    conn = sqlite3.connect('Lianjia.db')
    cu = conn.cursor()
    cu.execute(save_sql,data)
    conn.commit()
    conn.close()
