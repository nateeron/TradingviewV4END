import websocket
import json
import pprint
def on_message(ws, message):
    data = json.loads(message)
    current_price = float(data['c'])
    print(current_price)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("WebSocket closed")

def on_open(ws):
    # Subscribe to the real-time price updates for the given symbol
    symbol = 'btcusdt'
    XRPusdt = 'xrpusdt'
    data = ws.send(json.dumps({"method": "SUBSCRIBE", "params": [f"{XRPusdt}@ticker"], "id": 1}))
    print("-------------------------------data----------------------------")
    print(data)

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/xrpusdt@trade", on_message = on_message, on_error = on_error, on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()