from fastapi import FastAPI, WebSocket
import websocket
import json
app = FastAPI()



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
    # price = float(trade['p']) 
    
    # if use @kline_
    price = float(trade['k']['c']) 
    # symbo = trade['s']
    
    print('------------start-------------')
    print(price)
    # order_manager = FN_buy.OrderManager()  # Create an instance of OrderManager
    # order_manager.check_price_buy(price,symbo)
    
    # order_manager = FN_sell.OrderManager()  # Create an instance of OrderManager
    # order_manager.check_price_sell(price,symbo)
  
@app.get('/')
def read_root():
     return "OK Run Future Binace vsesion 1.0"

if __name__ == "__main__":
    import uvicorn
    websocket.enableTrace(True)
    # ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/xrpusdt@trade",
    # ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/xrpusdt@aggTrade",
    ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/xrpusdt@kline_1m",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
    uvicorn.run(app,  port=854)
