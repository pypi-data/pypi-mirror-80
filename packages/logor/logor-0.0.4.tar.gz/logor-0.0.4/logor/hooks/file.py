# coding: utf-8
import time
import uuid

from logor.interface import IHook


class FileHook(IHook):

    def __init__(self):
        self.o = open("logor.log", "w+", encoding="utf-8")

    def process_msg(self, msg: str) -> None:
        self.o.write(f"{msg}\n")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.o.close()


class RotateFileHook(IHook):

    def __init__(self):
        self.maxSize = 1024 * 1024 * 10
        self.o = None
        self.rotate()

    def process_msg(self, msg: str) -> None:
        self.o.seek(0, 2)
        if self.o.tell() > self.maxSize:
            self.rotate()
        self.o.write(f"{msg}\n")

    def rotate(self):
        if self.o:
            self.o.close()
        self.o = open(f"logor_{int(time.time())}_{str(uuid.uuid4()).replace('-', '')}.log", "w+", encoding="utf-8")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.o.close()


class TimeFileHook(IHook):

    def __init__(self):
        self.interval = 3600  # one hour
        self.last = None
        self.o = None
        self.rotate()

    def process_msg(self, msg: str) -> None:
        if int(time.time()) > (self.last + self.interval):
            self.rotate()
        self.o.write(f"{msg}\n")

    def rotate(self):
        if self.o:
            self.o.close()
        self.o = open(f"logor_{int(time.time())}_{str(uuid.uuid4()).replace('-', '')}.log", "w+", encoding="utf-8")
        self.last = int(time.time())

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.o.close()
