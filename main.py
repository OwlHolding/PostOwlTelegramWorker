import logging
import json
import threading
import uvicorn
import os
import asyncio
from fastapi import FastAPI

import parser
import client
import store

logging.basicConfig(level=logging.INFO, format="%(levelname)s:     %(asctime)s - %(message)s", filename="log.txt",
                    filemode="w")

with open("config.json", 'rb') as file:
    config = json.load(file)

logging.info("Config loaded")
unit = parser.Parser(config)
cli = client.Client(config)
channels = store.ChannelsStore(config)

if os.path.exists('channels'):
    channels.load_store()

logging.info("Modules inited")

app = FastAPI()


@app.post("/add-channel/{channel}/")
def add(channel: str):
    if channel in channels.list:
        channels.del_channel(channel)
        unit.del_channel(channel)
        return True
    else:
        return False


@app.post("/del-channel/{channel}/")
def del_channel(channel: str):
    if not (channel in channels.list):

        if len(channels.list) >= config['max_channel']:
            return False

        channels.add_channel(channel)
        unit.add_channel(channel)
        return True
    else:
        return True


logging.info("Start threading")
loop = asyncio.new_event_loop()

parser_thread = threading.Thread(target=unit.start, args=[cli.send_post, loop])
parser_thread.start()

logging.info("Parser started")
logging.info("Server started")

uvicorn.run(
    app=app,
    host=config['server_host'],
    port=config['server_port']
)
try:
    loop.stop()
except RuntimeError:
    pass
logging.info('Finishing process')

