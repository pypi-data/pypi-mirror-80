import asyncio

from watchgod import DefaultDirWatcher, watch
from threading import Thread


class ContentWatcher(DefaultDirWatcher):
    def should_watch_file(self, entry):
        return entry.name.endswith('.md')

class Watcher:
    def __init__(self, content_folder, nabu_obj, watcher_cls=ContentWatcher):
        self.content_folder = content_folder
        self.watcher_cls = watcher_cls
        self.nabu = nabu_obj
        self.stop_event = asyncio.Event()

    def start(self):
        self.thread = Thread(target=self.run)
        self.thread.start()
        print("Watcher started!")

    def shutdown(self):
        self.stop_event.set()

    def run(self):
        for changes in watch(self.content_folder, stop_event=self.stop_event, watcher_cls=self.watcher_cls):
            self.nabu.render_to_file()
