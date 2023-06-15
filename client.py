from requests_futures.sessions import FuturesSession
import logging


class Client:

    def __init__(self, config):
        self.session = FuturesSession()
        self.webhook = config['main_server_url']
        logging.info("Client: inited")

    async def send_post(self, channel, text):
        self.session.post(
            url=self.webhook,
            data={
                'channel': channel,
                'text': text
            }
        )
        logging.info('Client: post was sent')
