import os
import asyncio
import websockets
import json
import logging
from dotenv import load_dotenv

load_dotenv(override=True)
logger = logging.getLogger()

artifact_api_token = os.environ.get("artifact_api_token")
artifact_ws_host = os.environ.get("artifact_ws_host")

message = {
        "token": artifact_api_token,
        "subscriptions": ["event_spawn", "event_removed", "grandexchange_neworder", "grandexchange_sell", "achievement_unlocked"]
    }
 
async def receive_messages():
    async with websockets.connect(artifact_ws_host) as websocket:
        await websocket.send(json.dumps(message))

        logger.info("Connected to the WebSocket server")
        try:
            while True:
                message_received = await websocket.recv()
                message_received = json.loads(message_received)

                # TODO: add callback registry so callbacks can be triggered when messages are received here

        except websockets.ConnectionClosed:
            logger.info("Connection closed by the server")

asyncio.run(receive_messages())