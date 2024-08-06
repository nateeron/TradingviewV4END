import sqlite3
import os


# เช็ก Data ว่าถูกสรา้งหรือยัง ถ้ายังให้สร้าง
def check_db_and_table():
    db_path = 'settings.db'

    # Check if the database file exists
    if not os.path.exists(db_path):
        create_table()
        create_tableOrder()
        return {"status": 200, "message": "Create NEW Data"}


# เชื่มต่อ data
def connect_db():
    return sqlite3.connect('settings.db')


# สรา้ง Data Table tb_setting
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tb_setting (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            APIKEY TEXT NOT NULL,
            SECRETKEY TEXT NOT NULL,
            ORDER_VAL INTEGER NOT NULL,
            PERCEN_BUY REAL NOT NULL,
            PERCEN_SELL REAL NOT NULL,
            SYMBOL TEXT NOT NULL,
            LINE_ADMIN TEXT NOT NULL,
            LINE_USER TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# สรา้ง Data Table tb_Order
def create_tableOrder():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tb_Order (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            SYMBOL TEXT NOT NULL,
            PRICE_BUY REAL NOT NULL,
            PRICE_SELL REAL NOT NULL,
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
def Select_tableOrder(status,limit):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, SYMBOL, PRICE_BUY, PRICE_SELL, STATUS, DATE_BUY, DATE_SELL 
        FROM tb_Order 
        WHERE STATUS = ? 
        ORDER BY PRICE_SELL 
        LIMIT ?
    ''', (status, limit))
    Order = cursor.fetchone()
    conn.close()
    return Order


# update Data Table tb_Order
def update_order_status(order_id, new_status):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tb_Order
        SET STATUS = ?
        WHERE id = ?
    ''', (new_status, order_id))
    conn.commit()
    conn.close()
    
# insert Data Table tb_Order
def Insert_tableOrder(SYMBOL, PRICE_BUY, PRICE_SELL, STATUS, DATE_BUY):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
       INSERT INTO tb_Order (SYMBOL, PRICE_BUY, PRICE_SELL, STATUS, DATE_BUY)
        VALUES (?, ?, ?, ?, ?)
    ''', (SYMBOL, PRICE_BUY, PRICE_SELL, STATUS, DATE_BUY))
    conn.commit()
    conn.close()

# Add Data tb_setting
def create_setting(api_key, secret_key, order_val, perc_buy, perc_sell, symbol, line_admin, line_user):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tb_setting (APIKEY, SECRETKEY, ORDER_VAL, PERCEN_BUY, PERCEN_SELL, SYMBOL, LINE_ADMIN, LINE_USER)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (api_key, secret_key, order_val, perc_buy, perc_sell, symbol, line_admin, line_user))
    conn.commit()
    conn.close()

# Read tb_setting
def read_setting(setting_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tb_setting WHERE id = ?', (setting_id,))
    setting = cursor.fetchone()
    conn.close()
    return setting

# update tb_setting
def update_setting(setting_id, api_key=None, secret_key=None, order_val=None, perc_buy=None, perc_sell=None, symbol=None, line_admin=None, line_user=None):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Prepare the update statement
    updates = []
    params = []
    
    if api_key is not None:
        updates.append("APIKEY = ?")
        params.append(api_key)
    if secret_key is not None:
        updates.append("SECRETKEY = ?")
        params.append(secret_key)
    if order_val is not None:
        updates.append("ORDER_VAL = ?")
        params.append(order_val)
    if perc_buy is not None:
        updates.append("PERCEN_BUY = ?")
        params.append(perc_buy)
    if perc_sell is not None:
        updates.append("PERCEN_SELL = ?")
        params.append(perc_sell)
    if symbol is not None:
        updates.append("SYMBOL = ?")
        params.append(symbol)
    if line_admin is not None:
        updates.append("LINE_ADMIN = ?")
        params.append(line_admin)
    if line_user is not None:
        updates.append("LINE_USER = ?")
        params.append(line_user)
    if updates:
        update_statement = "UPDATE tb_setting SET " + ", ".join(updates) + " WHERE id = ?"
        params.append(setting_id)
        cursor.execute(update_statement, params)
        conn.commit()
    
    conn.close()
    
def delete_setting(setting_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tb_setting WHERE id = ?', (setting_id,))
    conn.commit()
    conn.close()


