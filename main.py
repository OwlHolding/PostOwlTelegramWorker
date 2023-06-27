import logging
import json
import threading
import uvicorn
import os
import asyncio
from fastapi import FastAPI, Response

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
def add(channel: str) -> Response:
    if not (channel in channels.list):
        if len(channels.list) >= config['max_channels']:
            return Response(status_code=507)

        channels.add_channel(channel)
        unit.add_channel(channel)
        return Response(status_code=201)
    else:
        return Response(status_code=208)


@app.post("/del-channel/{channel}/")
def del_channel(channel: str) -> Response:
    if channel in channels.list:
        channels.del_channel(channel)
        unit.del_channel(channel)
        return Response(status_code=205)
    else:
        return Response(status_code=404)


logging.info("Start threading")
loop = asyncio.new_event_loop()

parser_thread = threading.Thread(target=unit.start, args=[cli.send_post, loop])
parser_thread.start()

logging.info("Parser started")
logging.info("Server started")

uvicorn.run(
    app=app,
    host=config['host'],
    port=config['port']
)
try:
    loop.stop()
except RuntimeError:
    pass
logging.info('Finishing process')
