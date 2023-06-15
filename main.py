import logging
import json
import threading

import parser
import client
import server
import store
import os

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


def add_handler(channel: str) -> bool:
    if not (channel in channels.list):

        if len(channels.list) >= config['max_channel']:
            return False

        channels.add_channel(channel)
        unit.add_channel(channel)
        return True
    else:
        return True


def del_handler(channel: str):
    if channel in channels.list:
        channels.del_channel(channel)
        unit.del_channel(channel)
        return True
    else:
        return False


ser = server.Server(config, add_handler, del_handler)

logging.info("Modules inited")

server_thread = threading.Thread(target=ser.start)
server_thread.start()

unit.start(cli.send_post)
logging.info('Finishing process')
