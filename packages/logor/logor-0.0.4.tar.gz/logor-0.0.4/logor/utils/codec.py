# coding: utf-8
import struct
import socket

__all__ = "decode_msg", "encode_msg", "STOP",

STOP = b"\x00\xff\xff\xff\xff\xff\xff\xff\xff"


def decode_msg(sock: socket.socket) -> (str, int, bool):
    """
    receive a socket, then calculate the msg length
    :param sock:
    :return:
    """
    token = sock.recv(9)
    if token == STOP:
        return "", 0, True
    level, msg_length, = struct.unpack('!BQ', token)
    msg = sock.recv(msg_length)
    return msg.decode("utf-8"), level, False


def encode_msg(msg: str, level: int) -> bytes:
    """
    get a msg-bytes length and calculate teh token
    :param msg:
    :return:
    """
    msg = msg.encode("utf-8")
    msg_length = len(msg)
    token = struct.pack("!BQ", level, msg_length)
    return token + msg
