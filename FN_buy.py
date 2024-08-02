import json
import datetime
import time
# Load the JSON data from the file
import pprint as pprint
import FN_calAction as ta
import mysql_Query as qury
import BotSpot
# with open('data.json') as f:
#     data = json.load(f)

# # Save the updated JSON data back to the file
# with open('data.json', 'w') as f:
#     json.dump(data, f, indent=4) # Save with indentation for better readability
    
# # Extract the "Order" list from the data
# orders = data["Order"]
# cound = len(orders)
# print('cound1 : ',cound)
# # Filter orders where the "buy" value is greater than or equal to 0.5455
# filtered_orders = [order for order in orders if float(order["buy"]) == 64564 or float(order["buy"]) == 6457764 ]
# cound2 = len(filtered_orders)
# print('cound2 : ',cound2)
# print('data : ',filtered_orders)
# Print the filtered orders
# for order in filtered_orders:
#     print(order)
ISDOING_ACTION = 0


class OrderManager:
    def __init__(self):
        with open('config.json') as f:
            config = json.load(f)
        self.config = config
        
        
    def check_price_buy(self,pri,symbol):
        try:
            priceActionLast = 999999999.99
            price = float(pri)
            # Get data last Buy
            order_json = qury.select_order_last(symbol)
            if order_json != []:
                #order_json = order_json
                order = json.loads(order_json) if order_json else None
                if order:
                    status = order[0]['status'] # from SQL data
                    # ถ้ายังไม่ขาย ให้นับจุดซื้อล่าสุด ลงมา
                    if status == 1:
                        priceActionLast = float(order[0]['Price_Sell'])
                    else:
                        priceActionLast = float(order[0]['Price'])
               
                
            # Check buy 
            next_Buy,percenB =  ta.calAction_Buy(priceActionLast,self.config)
            
            next_Buy = ta.f4(next_Buy)
            
            print('#######[ Check Buy ]#######')
            print('is :',price <= next_Buy)
            # ถ้าขาย ได้ไม้คืน จุกซื้อถึดไปจะนับจากจุดขายล่าสุด ลงมา 
            print("price <= next_Buy: ",price ,'<=',next_Buy ,' %percenB :',percenB ,' priceActionLast :',priceActionLast)
            # Check Sell
            OrderSell = qury.select_order_willSell(symbol)
            
            if price <= next_Buy :
            #if True:
                print("Action BUY")
                order_quantity =float(self.config['ORDER_VAL'])
                #  buy  sell
                Price_Action =BotSpot.trad(symbol,'buy',order_quantity,'','','')
                # # เมื่อซื้อเสร็จ ให้ SAVE ราคาขาย
                quantity = ta.f2( order_quantity/price )
                P_Sell ,percenS =  ta.calAction_Sell(Price_Action,self.config)
                qury.insert_Order(symbol, Price_Action,ta.f4(P_Sell),quantity)
                    
            
            print('#######[ Check Sell ]#######')
           
            for item in OrderSell:
                print('IF Market > mySell')
                print( price,'>=', item['Price_sell'],price >= float(item['Price_sell']))
                
                if price >= float(item['Price_sell']) :
                    print("Action SELL")
                    Price_Action =BotSpot.trad(symbol,'sell',item['Quantity'],'','','')
                    priceSell = price
                    qury.Update_sellOrder(item['OrderActionID'],priceSell)
        except Exception as e:
          print('An exception occurred',e)




order_manager_ = OrderManager()
order_manager_.check_price_buy('0.5508','XRPUSDT')
# current_timestamp = time.time()
# print(current_timestamp)
# current_datetime = datetime.datetime.fromtimestamp(current_timestamp)
# print(current_datetime.strftime('%Y-%m-%d %H:%M:%S'))
    