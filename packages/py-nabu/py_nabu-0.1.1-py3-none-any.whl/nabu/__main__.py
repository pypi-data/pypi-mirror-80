import sys

from threading import Thread

from .nabu import NabuConfig, Nabu
from .watch import Watcher
from .serve import Server


def main(mode='render'):
    config = NabuConfig()
    n = Nabu(config)
    n.render_to_file()

    if mode == 'serve':
        server = Server(config['output_folder'], 8080)
        watcher = Watcher(config['content_folder'], n)

        server.start()
        watcher.start()

        try:
            while watcher.thread.is_alive():
                server.thread.join(0.1)
                watcher.thread.join(0.1)

        except KeyboardInterrupt:
            print('Stopping...')
            server.shutdown()
            watcher.shutdown()

            server.thread.join()
            watcher.thread.join()
        
    return n

if __name__ == "__main__":
    kwargs = {}

    if len(sys.argv) > 1:
        if sys.argv[1] == 'serve':
            kwargs.update(mode='serve')

    o = main(**kwargs)
