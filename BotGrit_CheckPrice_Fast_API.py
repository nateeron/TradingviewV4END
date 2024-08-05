import threading
import time
import websocket
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import SQLite as qry
import BotGrit_CheckPrice_Fast_API_FN_buy as FN_buy

app = FastAPI()
ws_thread = None
ws_thread2 = None
ws = None
ws2 = None
should_run = False
should_run2 = False
price1 = [{"E":99999999,'p': 0.0}]

async def on_message(ws, message):
    data = json.loads(message)
    if price1[0]["E"] != data["E"] and  price1[0]["p"] != data["p"]:
        print(data["s"],data["p"],55)
        print('------------start-------------')
        symbo = data['s']
        price = float(data['p']) 
        print(symbo,price)
        order_manager =FN_buy.OrderManager()  # Create an instance of OrderManager
        resp = await order_manager.check_price_buy(price,symbo)
        # {'e': 'trade', 'E': 1722844176552, 's': 'XRPUSDT', 't': 641078642, 'p': '0.47220000', 'q': '1273.00000000', 'T': 1722844176546, 'm': False, 'M': True}
        if price1:
            price1.pop(0)
        price1.append({"E":data["E"],"p":data["p"]})

async def on_message2(ws, message):
    data = json.loads(message)
    if price1[0]["E"] != data["E"] and  price1[0]["p"] != data["p"]:
        print(data["s"],data["p"])
        print('------------start-------------')
        symbo = data['s']
        price = float(data['p']) 
        print(symbo,price)
        order_manager =FN_buy.OrderManager()  # Create an instance of OrderManager
        resp = await order_manager.check_price_buy(price,symbo)
        # {'e': 'trade', 'E': 1722844176552, 's': 'XRPUSDT', 't': 641078642, 'p': '0.47220000', 'q': '1273.00000000', 'T': 1722844176546, 'm': False, 'M': True}
        if price1:
            price1.pop(0)
        price1.append({"E":data["E"],"p":data["p"]})
    
def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed")

def on_open(ws):
    print("WebSocket connection opened")

def run_websocket():
    global ws
    ws = websocket.WebSocketApp(
        "wss://stream.binance.com:9443/ws/xrpusdt@trade",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()
    
def run_websocket2():
    global ws2
    ws2 = websocket.WebSocketApp(
        "wss://stream.binance.com:9443/ws/bnbusdt@trade",
        on_message=on_message2,
        on_error=on_error,
        on_close=on_close
    )
    ws2.on_open = on_open
    ws2.run_forever()

@app.post("/start")
def start_websocket():
    global ws_thread, should_run
    if ws_thread is None or not ws_thread.is_alive():
        should_run = True
        ws_thread = threading.Thread(target=run_websocket)
        ws_thread.start()
        return JSONResponse(content={"message": "WebSocket connection started"})
    else:
        return JSONResponse(content={"message": "WebSocket connection is already running"})

@app.post("/start2")
def start_websocket():
    global ws_thread2, should_run2
    if ws_thread2 is None or not ws_thread2.is_alive():
        should_run2 = True
        ws_thread2 = threading.Thread(target=run_websocket2)
        ws_thread2.start()
        return JSONResponse(content={"message": "WebSocket connection started"})
    else:
        return JSONResponse(content={"message": "WebSocket connection is already running"})

@app.post("/st_all")
def start_websocket():
    global ws_thread, should_run,ws_thread2, should_run2
 
    txt = []
    if ws_thread is None or not ws_thread.is_alive():
        should_run = True
        ws_thread = threading.Thread(target=run_websocket)
        ws_thread.start()
        txt.append(JSONResponse(content={"message 1": "WebSocket connection started"}))
    else:
        txt.append(JSONResponse(content={"message 1": "WebSocket connection is already running"})) 
        
    if ws_thread2 is None or not ws_thread2.is_alive():
        should_run2 = True
        ws_thread2 = threading.Thread(target=run_websocket2)
        ws_thread2.start()
        print("asdasd")
        txt.append(JSONResponse(content={"message 2": "WebSocket connection started"}))
    else:
        txt.append(JSONResponse(content={"message 2": "WebSocket connection is already running"})) 
    return txt

@app.post("/stop")
def stop_websocket():
    global should_run, ws
    should_run = False
    if ws is not None:
        ws.close()
    return JSONResponse(content={"message": "WebSocket connection stopped"})

@app.post("/stop2")
def stop_websocket():
    global should_run2, ws2
    should_run2 = False
    if ws2 is not None:
        ws2.close()
    return JSONResponse(content={"message": "WebSocket connection stopped"})


@app.post("/stop_all")
def stop_websocket():
    global should_run2, ws2
    should_run2 = False
    if ws2 is not None:
        ws2.close()
    global should_run, ws
    should_run = False
    if ws is not None:
        ws.close()
    
    return JSONResponse(content={"message": "WebSocket connection stopped"})

# ดูการตั้งค่า Setting.Json
@app.get("/setting")
def stop_websocket():
    resp = qry.check_db_and_table()
    print(resp)
    with open('config.json') as f:
        config = json.load(f)
    return config

# Define the Pydantic model
class Settings(BaseModel):
    api_key: str
    secret_key: str
    order_val: int
    perc_buy: float
    perc_sell: float
    symbol: str
    line_admin: str
    line_user: str

# Add Data SQLite
@app.post("/addData")
def add_data(settings: Settings):
   
    try:
        print(settings)
        qry.create_setting(
            api_key=settings.api_key,
            secret_key=settings.secret_key,
            order_val=settings.order_val,
            perc_buy=settings.perc_buy,
            perc_sell=settings.perc_sell,
            symbol=settings.symbol,
            line_admin=settings.line_admin,
            line_user=settings.line_user
        )
        
        return {"message": "Success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add Data SQLite
# get Order 
@app.post("/get_Order")
def add_data(settings: Settings):
   
    try:
        print(settings)
        qry.create_setting(
            api_key=settings.api_key,
            secret_key=settings.secret_key,
            order_val=settings.order_val,
            perc_buy=settings.perc_buy,
            perc_sell=settings.perc_sell,
            symbol=settings.symbol,
            line_admin=settings.line_admin,
            line_user=settings.line_user
        )
        
        return {"message": "Success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    

# ทำการตั้งค่า
class APIKey(BaseModel):
    KEY: Optional[str] = None
    SECRETKEY: Optional[str] = None

class Connection(BaseModel):
    DATA_HOST: Optional[str] = None
    DATA_PORT: Optional[str] = None
    DATA_USER: Optional[str] = None
    DATA_PASSWORD: Optional[str] = None
    DATA_NAME: Optional[str] = None
    LINE_ADMIN: Optional[str] = None
    LINE_ADMIN2: Optional[str] = None

class ConnetBinace(BaseModel):
    API_KEY: Optional[str] = None
    API_SECRET: Optional[str] = None
    LINE_ADMIN: Optional[str] = None
    LINE_ADMIN2: Optional[str] = None

class Config(BaseModel):
    APIKEY: Optional[APIKey] = None
    ORDER_VAL: Optional[str] = None
    PERCEN_BUY: Optional[str] = None
    PERCEN_SELL: Optional[str] = None
    SYMBOL: Optional[List[str]] = None
    Connetion: Optional[Connection] = None
    ConnetBinace: Optional[ConnetBinace] = None
    
@app.post("/setting")
def update_settings(new_config: Config):
    try:
        # Read the current config
        with open('config.json', 'r') as f:
            current_config = json.load(f)
        
        # Update the current config with new values
        def update_dict(original: Dict, updates: Dict) -> Dict:
            for key, value in updates.items():
                if isinstance(value, dict) and key in original:
                    original[key] = update_dict(original[key], value)
                else:
                    original[key] = value
            return original
        
        updated_config = update_dict(current_config, new_config.dict(exclude_unset=True))
        
        # Write the updated config back to the file
        with open('config.json', 'w') as f:
            json.dump(updated_config, f, indent=4)
        
        return {"message": "Configuration updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    print("ok")
    uvicorn.run(app,  port=8400, log_level="debug", reload=True)
    
    
# Run TEST
# uvicorn BotGrit_CheckPrice_Fast_API:app --host 127.0.0.1 --port 8400 --log-level debug --reload