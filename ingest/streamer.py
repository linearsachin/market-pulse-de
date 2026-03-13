import websocket
import json
import pandas as pd
import os
import sys

# Ensure the ingest folder is in the python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the helpers
from utils import get_db, logger, get_config

buffer = []

def on_message(ws, message):
    global buffer
    try:
        data = json.loads(message)
        
        if data.get('type') == 'trade':
            for t in data['data']:
                buffer.append({
                    'symbol': t['s'], 
                    'price': t['p'], 
                    'volume': t['v'], 
                    'ts': t['t']
                })
            
            # Check if buffer is full
            if len(buffer) >= 50:
                df = pd.DataFrame(buffer)
                
                # --- THE FIX ---
                # Call get_db() here. It is now explicitly imported above.
                con = get_db() 
                con.execute("CREATE TABLE IF NOT EXISTS bronze_trades AS SELECT * FROM df WHERE 1=0")
                con.append("bronze_trades", df)
                con.close()
                # ----------------
                
                logger.info(f"✅ Successfully saved {len(buffer)} trades to DuckDB")
                buffer = []
                
    except Exception as e:
        # This will now tell us exactly if it's still a naming issue or something else
        logger.error(f"❌ Callback Error: {str(e)}")

def on_error(ws, error):
    logger.error(f"WS Error: {error}")

def on_close(ws, close_status_code, close_msg):
    logger.info("### Websocket Closed ###")

def on_open(ws):
    config = get_config()
    symbols = config.get('symbols', [])
    for s in symbols:
        ws.send(json.dumps({"type":"subscribe","symbol":s}))
    logger.info(f"🚀 Subscribed to {symbols}")

if __name__ == "__main__":
    # Create the websocket app
    ws = websocket.WebSocketApp(
        f"wss://ws.finnhub.io?token={os.getenv('FINNHUB_API_KEY')}",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )
    ws.run_forever()