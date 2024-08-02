import mysql.connector
from line_notify import LineNotify
import json
import datetime
import time
import pprint as pprint
with open('config.json') as f:
    dataconfig = json.load(f)
Connetion = dataconfig["Connetion"]

notify = LineNotify(Connetion['LINE_ADMIN'])
notify2 = LineNotify(Connetion['LINE_ADMIN2'])



def connect_mysql():
    try:
        
        return mysql.connector.connect(host=Connetion['DATA_HOST'], port=Connetion['DATA_PORT'],
                                       user="root", password=Connetion['DATA_PASSWORD'], database=Connetion['DATA_NAME'])
    except:
       pass
   

def select_order_willSell(sym):
    try:
        db = connect_mysql()
        cursor = db.cursor(dictionary=True)
        sql = "call select_order_willSell('{0}')".format(sym)
        cursor.execute(sql)
        data = cursor.fetchall()
        

    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

    finally:
        cursor.close()
        db.close()
        return(data)
    
def select_order_last(sym):
    try:
        db = connect_mysql()
        cursor = db.cursor(dictionary=True)
        sql = "call select_order_last('{0}')".format(sym)
        cursor.execute(sql)
        data = cursor.fetchall()
        pprint(data)
        #data = cursor.fetchone()  # fetchone since you are only expecting a single row
          # Convert the dictionary to a JSON string

    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

    finally:
        cursor.close()
        db.close()
        return json.dumps(data)
    
def Update_sellOrder(id, Price):
    try:
        db = connect_mysql()
        cursor = db.cursor()
        sql = "call Update_sellOrder('{0}',{1})".format(id,Price)
        cursor.execute(sql)
        db.commit()
        text ='🔴Sell ID : {0} price : {1}'.format(id,Price) 
        notify.send(text)

    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

    finally:
        cursor.close()
        db.close()
       
def insert_Order(symbol, Price,P_Sell,quantity):
    try:
        db = connect_mysql()
        cursor = db.cursor()
        sql = "call insert_Order('{0}',{1},{2},{3})".format(symbol,Price,P_Sell,quantity)
        print(sql)
        cursor.execute(sql)
        db.commit()
        text ='🟢Buy {0} price : {1} to Sell : {2},quantity {3}'.format(symbol, Price,P_Sell,quantity) 
        notify.send(text)

    except mysql.connector.Error as error:
        print("Failed to execute stored procedure: {}".format(error))

    finally:
        cursor.close()
        db.close()
    
# ss = select_order_willSell('xrpusdt', 0)
# print(ss)

