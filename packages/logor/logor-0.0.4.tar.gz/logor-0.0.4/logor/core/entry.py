# coding: utf-8
import json
import socket
import datetime

from logor.utils import *
from logor.core.socket_manager import SocketManager


def check_log_level(level: int = None):
    def wrapper(*args, **kwargs):
        def _wrapper(entry, msg: str):
            basic_level = SocketManager.level if entry.level is None else \
                entry.level
            if level < basic_level:  # check log level
                return
            entry.send_msg(msg, level)

        return _wrapper

    return wrapper


class Entry:

    def __init__(self, module: str, level: int = None, sock: socket.socket = None):
        self.module = module
        self.level = level
        self.fields = dict()
        self.text_fields = ""
        self.sock = sock or SocketManager.get_client()
        self.std_text = True if SocketManager.stdMode.startswith("text") else False

    def setLevel(self, level: int):
        assert level in level_map, "ensure your log level validity"
        self.level = level

    def setFields(self, fields: dict) -> None:
        self.fields.update(fields)
        text_fields = ""
        for key, value in self.fields.items():
            text_fields += f"{key}={value} "
        self.text_fields = text_fields

    def send(self, msg: str, level: int) -> None:
        self.sock.send(encode_msg(msg, level))

    def json_msg(self, msg: str, level: int) -> None:
        json_msg = {
            "time": f"{datetime.datetime.now()}",
            "level": level_map.get(level, "unknown"),
            "msg": msg,
        }
        json_msg.update(self.fields)
        self.send(json.dumps(json_msg, ensure_ascii=False), level)

    def text_msg(self, msg: str, level: int) -> None:
        text_msg = f'time="{datetime.datetime.now()}" level={level_map.get(level, "unknown")} msg="{msg}" {self.text_fields}'
        self.send(text_msg, level)

    def send_msg(self, msg: str, level: int) -> None:
        if self.std_text:
            self.text_msg(msg, level)
        else:
            self.json_msg(msg, level)

    @check_log_level(level=DEBUG)
    def debug(self, msg: str):
        raise NotImplementedError

    @check_log_level(level=INFO)
    def info(self, msg: str):
        raise NotImplementedError

    @check_log_level(level=WARNING)
    def warning(self, msg: str):
        raise NotImplementedError

    @check_log_level(level=ERROR)
    def error(self, msg: str):
        raise NotImplementedError


class EntryMap:
    entryMap = dict()

    @classmethod
    def get(cls, module: str = None) -> Entry:
        if module not in cls.entryMap:
            SocketManager.init_socketpair()
            cls.entryMap[module] = Entry(module)
        return cls.entryMap[module]
