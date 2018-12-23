import sqlite3

def create_db():
    conn = sqlite3.connect('Lianjia.db')
    cu = conn.cursor()
    conn.close()
    print("Create_db success")

def create_table():
    conn = sqlite3.connect('Lianjia.db')
    cu = conn.cursor()
    cu.execute('''CREATE TABLE 'table_1223' (
        'HousePos',
        'Cells',
        'High',
        'TotalH',
        'HouseYear',
        'HouseType',
        'HouseSize',
        'TotalP',
        'UnitP',
        'HouseInter',
        'HouseUrl'
        )''')
    print("Create_table table_1223 success")
    conn.commit()
    conn.close()

def update_table(HousePos,Cells,High,TotalH,HouseYear,HouseType,HouseSize,TotalP,UnitP,HouseInter,HouseUrl):
    save_sql = 'INSERT INTO table_1223 values (?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?)'
    data = (HousePos,Cells,High,TotalH,HouseYear,HouseType,HouseSize,TotalP,UnitP,HouseInter,HouseUrl)
    conn = sqlite3.connect('Lianjia.db')
    cu = conn.cursor()
    cu.execute(save_sql,data)
    conn.commit()
    conn.close()
