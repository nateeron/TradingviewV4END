import sqlite3
import os
from datetime import datetime

# เช็ก Data ว่าถูกสรา้งหรือยัง ถ้ายังให้สร้าง
def check_db_and_table():
    db_path = 'settings.db'
    # Check if the database file exists
    if not os.path.exists(db_path):
        create_table_order()
        return {"status": 200, "message": "Create NEW Data"}


# เชื่มต่อ data
def connect_db():
    return sqlite3.connect('settings.db')



# สรา้ง Data Table tb_Order
def create_table_order():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tb_Order (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            SYMBOL TEXT NOT NULL,
            PRICE_BUY REAL NOT NULL,
            PRICE_SELL REAL NOT NULL,
            QUANTITY REAL NOT NULL,
            STATUS INTEGER NOT NULL,
            DATE_BUY TEXT NOT NULL,
            DATE_SELL TEXT
        )
    ''')
    conn.commit()
    conn.close()
    
# id	Price_Buy	Price_Sell	status	dateBuy	dateSell
# 1	0.4586	0.4686	1	28/7/2024	28/7/2024
# select Data Table tb_Order
def Select_tableOrder(status,symbol,orderby,limit):
    conn = connect_db()
    cursor = conn.cursor()
    # status 0 not Sell
    cursor.execute('''
        SELECT id, SYMBOL, PRICE_BUY, PRICE_SELL,QUANTITY, STATUS, DATE_BUY, DATE_SELL 
        FROM tb_Order 
        WHERE STATUS = ? and SYMBOL = ?
        ORDER BY ? 
        LIMIT ?
    ''', (status, symbol ,orderby,limit))
    Order = cursor.fetchone()
    conn.close()
    return Order


# update Data Table tb_Order
def update_order_status(order_id, new_status,priceSell):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tb_Order
         SET PRICE_SELL = ?,STATUS = ?,
            DATE_SELL = ?
        WHERE id = ?
    ''', (priceSell,new_status, datetime.now().isoformat(), order_id))
    conn.commit()
    conn.close()
    
# insert Data Table tb_Order
def Insert_tableOrder(SYMBOL, PRICE_BUY, PRICE_SELL, STATUS, QUANTITY):
    conn = connect_db()
    cursor = conn.cursor()
    DATE_BUY = datetime.now().isoformat()
    cursor.execute('''
       INSERT INTO tb_Order (SYMBOL, PRICE_BUY, PRICE_SELL,QUANTITY, STATUS, DATE_BUY, DATE_SELL)
        VALUES (?, ?, ?, ?, ?, ?,?)
    ''', (SYMBOL, PRICE_BUY, PRICE_SELL,QUANTITY, STATUS, DATE_BUY,DATE_BUY))
    conn.commit()
    conn.close()


# DELETE tb_Order BY ID
def delete_setting(setting_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tb_Order WHERE id = ?', (setting_id,))
    conn.commit()
    conn.close()


