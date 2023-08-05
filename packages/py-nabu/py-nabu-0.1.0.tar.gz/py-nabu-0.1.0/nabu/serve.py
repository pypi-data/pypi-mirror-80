import socket

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread


class CustomDirHTTPRequestHandlerFactory:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def __call__(self, *args, **kwargs):
        return SimpleHTTPRequestHandler(*args, **kwargs, directory=self.output_dir)

class Server:
    def __init__(self, output_dir, port):
        handler = CustomDirHTTPRequestHandlerFactory(output_dir)
        srv_class = ThreadingHTTPServer

        infos = socket.getaddrinfo(
            None,
            port,
            type=socket.SOCK_STREAM,
            flags=socket.AI_PASSIVE,
        )
        srv_class.address_family, _, _, _, addr = next(iter(infos))

        handler.protocol = "HTTP/1.0"

        self.httpd = srv_class(addr, handler)
        self.host, self.port = self.httpd.socket.getsockname()[:2]

    def start(self):
        self.thread = Thread(target=self.run)
        self.thread.start()
        print("HTTP server running:", self.port)

    def shutdown(self):
        self.httpd.shutdown()

    def run(self):
        self.httpd.serve_forever()
