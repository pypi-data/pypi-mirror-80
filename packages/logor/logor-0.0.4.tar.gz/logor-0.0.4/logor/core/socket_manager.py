# coding: utf-8
import atexit
import socket
import threading

from logor.utils import *


def _python_exit():
    client = SocketManager.get_client()
    client.send(STOP)
    for top in thread_or_process:
        top.join()


atexit.register(_python_exit)


class SocketManager:
    server = None
    client = None

    level = INFO  # global attr
    stdMode = "text/json"  # global attr

    lock = threading.Lock()

    @classmethod
    def init_socketpair(cls) -> None:
        if cls.server or cls.client:
            return
        with cls.lock:
            if cls.server or cls.client:
                return
            cls.server, cls.client = socket.socketpair()

    @classmethod
    def clear(cls) -> None:
        cls.server = None
        cls.client = None

    @classmethod
    def get_server(cls) -> socket.socket:
        if not cls.server:
            cls.init_socketpair()
        return cls.server

    @classmethod
    def get_client(cls) -> socket.socket:
        if not cls.client:
            cls.init_socketpair()
        return cls.client
