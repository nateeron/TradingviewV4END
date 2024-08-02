import websocket
import json
import FN_buy


def on_error(ws, error):
    print('error')
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("### opened ###")


def on_message(ws, message):
    # Parse the JSON message
    trade = json.loads(message)
    # Extract the price from the trade message
    # if use @aggTrade or  @trade
    price = float(trade['p']) 
    
    # if use @kline_
    # price = float(trade['k']['c']) 
    symbo = trade['s']
    
    print('------------start-------------')
    print(symbo,price)
    order_manager = FN_buy.OrderManager()  # Create an instance of OrderManager
    order_manager.check_price_buy(price,symbo)
    
    # order_manager = FN_sell.OrderManager()  # Create an instance of OrderManager
    #order_manager.check_price_sell(price,symbo)
    # Call the function to check the price
    #FN_buy.OrderManager.check_price_buy(price,symbo)
    #FN_sell.check_price_sell(price)


if __name__ == "__main__":
    
    websocket.enableTrace(True)
    # ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/xrpusdt@trade",
    # ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/xrpusdt@aggTrade",
    # ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/xrpusdt@kline_1m",bnbusdt
    ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/xrpusdt@trade",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
