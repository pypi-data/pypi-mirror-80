# coding: utf-8
import sys

from logor.interface import IHook


class StderrHook(IHook):

    def __init__(self):
        self.o = sys.stderr

    def process_msg(self, msg: str) -> None:
        self.o.write(f"{msg}\n")
        self.o.flush()


class StdoutHook(IHook):

    def __init__(self):
        self.o = sys.stdout

    def process_msg(self, msg: str) -> None:
        self.o.write(f"{msg}\n")
        self.o.flush()
