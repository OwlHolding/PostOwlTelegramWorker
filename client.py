import json

from requests_futures.sessions import FuturesSession
import logging


class Client:

    def __init__(self, config):
        self.session = FuturesSession()
        self.webhook = config['webhook']
        logging.info("Client: inited")

    async def send_post(self, channel, text):
        data = {
            'channel': channel,
            'text': text
        }

        json_data = json.dumps(data)

        self.session.post(
            url=self.webhook,
            data=json_data
        )
        logging.info('Client: post was sent')
