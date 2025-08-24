import websocket
import json
import time

from .event_processor import EventProcessor
from .constants import JUPITER_PROGRAM_ID, PUMP_FUN_PROGRAM_ID, RAYDIUM_V4_PROGRAM_ID, WSS_ENDPOINT

WSS = WSS_ENDPOINT

event_processor = EventProcessor()

def on_message(ws, message):
    try:
        log_data = json.loads(message)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return
    
    logs = log_data.get("params", {}) \
                   .get("result", {}) \
                   .get("value", {}) \
                   .get("logs", [])

    if not logs:
        return
    
    event = event_processor.process_logs(logs)
    if event:
        event_processor.handle_event(event)

def on_error(ws, error):
    print(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket connection closed")

def on_open(ws):
    # Subscribe to Jupiter program
    jupiter_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "logsSubscribe",
        "params": [
            {"mentions": [JUPITER_PROGRAM_ID]},
            {"commitment": "processed"},
        ],
    }
    
    # Subscribe to pump.fun program
    pump_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "logsSubscribe",
        "params": [
            {"mentions": [PUMP_FUN_PROGRAM_ID]},
            {"commitment": "processed"},
        ],
    }
    
    # Subscribe to Raydium V4 program
    raydium_request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "logsSubscribe",
        "params": [
            {"mentions": [RAYDIUM_V4_PROGRAM_ID]},
            {"commitment": "processed"},
        ],
    }
    
    try:
        ws.send(json.dumps(jupiter_request))
        print("Subscribed to Jupiter logs...")
        ws.send(json.dumps(pump_request))
        print("Subscribed to pump.fun logs...")
        ws.send(json.dumps(raydium_request))
        print("Subscribed to Raydium V4 logs...")
    except Exception as e:
        print(f"Error sending subscription request: {e}")

def start_websocket():
    while True:
        ws = websocket.WebSocketApp(
            WSS,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        ws.on_open = on_open
        ws.run_forever()
        print("WebSocket connection lost. Reconnecting in 1 second...")
        time.sleep(1)

if __name__ == "__main__":
    try:
        start_websocket()
    except Exception as e:
        print(f"Unexpected error in main event loop: {e}")