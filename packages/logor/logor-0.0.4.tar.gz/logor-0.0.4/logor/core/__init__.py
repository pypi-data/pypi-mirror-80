# coding: utf-8
import sys
import socket
import traceback

from logor.hooks import *


def log_serve(server: socket.socket) -> None:
    o = sys.stdout
    while True:
        try:
            msg, level, stop = decode_msg(server)
            if stop:
                break
            basic_hooks(msg)
            if level >= DEBUG:
                debug_hooks(msg)
            if level >= INFO:
                info_hooks(msg)
            if level >= WARNING:
                warning_hooks(msg)
            if level >= ERROR:
                error_hooks(msg)
        except:
            o.write(traceback.format_exc())
            break
    o.write("\nlogor serve stop\n")
    o.flush()
