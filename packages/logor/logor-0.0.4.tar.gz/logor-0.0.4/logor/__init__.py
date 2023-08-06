# coding: utf-8
import threading
import multiprocessing

from logor.hooks import register_hook
from logor.core import log_serve
from logor.core.entry import *
from logor.core.socket_manager import SocketManager


def withFields(fields: dict) -> Entry:
    entry = EntryMap.get()
    entry.setFields(fields)
    return entry


def getLogger(module) -> Entry:
    return EntryMap().get(module)


def setLevel(level: int):
    assert level in level_map, "please ensure your level valid"
    SocketManager.level = level


class Logor:

    def add_hooks(self, level: int, hooks: list):
        for hook in hooks:
            register_hook(level, hook)

    def __init__(self, module="", process=False, **kwargs):
        if process and module == "__main__":
            self.start_process = True
        else:
            self.start_process = False
        self.add_hooks(0, kwargs.get("basic_hooks", ["logor.hooks.console.StdoutHook"]))
        self.add_hooks(DEBUG, kwargs.get("debug_hooks", []))
        self.add_hooks(INFO, kwargs.get("info_hooks", []))
        self.add_hooks(WARNING, kwargs.get("warning_hooks", []))
        self.add_hooks(ERROR, kwargs.get("error_hooks", []))

    def __enter__(self):
        server = SocketManager.get_server()
        if self.start_process:
            p = multiprocessing.Process(target=log_serve, args=(server,), daemon=False)
            p.start()
            thread_or_process.append(p)
        else:
            t = threading.Thread(target=log_serve, args=(server,), daemon=True)
            t.start()
            thread_or_process.append(t)

    def __exit__(self, exc_type, exc_val, exc_tb):
        client = SocketManager.get_client()
        for top in thread_or_process:
            if hasattr(top, "terminate"):
                client.send(STOP)
