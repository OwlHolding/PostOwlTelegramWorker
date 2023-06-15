import logging
import os


class ChannelsStore:
    """Класс для хранения списка используемых каналов"""

    def __init__(self, config: dict):
        self.path = config['store_path']
        basedir = os.path.dirname(self.path)
        if not os.path.exists(basedir) and basedir:
            os.makedirs(basedir)
        open(self.path, 'a').close()
        self.list = []

        logging.info("Store: inited")

    def add_channel(self, channel: str) -> bool:
        if not (channel in self.list):
            self.list.append(channel)
            with open(self.path, 'w') as file:
                file.write("\n".join(self.list))
            return True
        else:
            return False

    def del_channel(self, channel: str) -> bool:
        if channel in self.list:
            self.list.pop(self.list.index(channel))
            with open(self.path, 'w') as file:
                file.write("\n".join(self.list))
            return True
        else:
            return False

    def load_store(self, path=None):
        if path:
            with open(path, 'r') as file:
                self.list = file.read().split('\n')
        else:
            with open(self.path, 'r') as file:
                self.list = file.read().split('\n')