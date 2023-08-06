# coding: utf-8
import threading
import multiprocessing

from typing import List

__all__ = ("DEBUG", "INFO", "WARNING", "ERROR", "level_map", "thread_or_process")

DEBUG: int = 10
INFO: int = 20
WARNING: int = 30
ERROR: int = 40
level_map: dict = {
    DEBUG: "debug",
    INFO: "info",
    WARNING: "warning",
    ERROR: "error",
}
thread_or_process = []  # type: List[multiprocessing.Process, threading.Thread]
