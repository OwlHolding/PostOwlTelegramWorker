from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import logging


class Server:
    """Класс для получения команд с главного сервера"""

    def __init__(self, config, add_channel_handler, del_channel_handler):
        class HttpHandler(BaseHTTPRequestHandler):
            def do_POST(self):
                if '/add-channel/' in self.path:
                    channel = self.path[self.path.rfind('/', 0, -1)+1:-1]
                    if add_channel_handler(channel):
                        self.send_response(201)
                        self.end_headers()
                    else:
                        self.send_response(423)
                        self.end_headers()
                elif '/del-channel/' in self.path:
                    channel = self.path[self.path.rfind('/', 0, -1)+1:-1]

                    if del_channel_handler(channel):
                        self.send_response(205)
                        self.end_headers()
                    else:
                        self.send_response(423)
                        self.end_headers()
                else:
                    self.send_response(404)
                    self.end_headers()

        self.server = HTTPServer((config['server_host'], config['server_port']), HttpHandler)

        logging.info("Server: inited")

    def start(self):
        logging.info("Server: Starting")
        self.server.serve_forever()
