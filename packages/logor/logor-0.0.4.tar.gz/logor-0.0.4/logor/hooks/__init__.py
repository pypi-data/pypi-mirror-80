# coding: utf-8
import re

from logor.utils import *
from typing import List
from logor.interface import IHook
from importlib import import_module

BASIC_HOOKS: List[IHook] = []
DEBUG_HOOKS: List[IHook] = []
INFO_HOOKS: List[IHook] = []
WARNING_HOOKS: List[IHook] = []
ERROR_HOOKS: List[IHook] = []


def basic_hooks(msg: str) -> None:
    for hook in BASIC_HOOKS:
        hook.process_msg(msg)


def debug_hooks(msg: str) -> None:
    for hook in DEBUG_HOOKS:
        hook.process_msg(msg)


def info_hooks(msg: str) -> None:
    for hook in INFO_HOOKS:
        hook.process_msg(msg)


def warning_hooks(msg: str) -> None:
    for hook in WARNING_HOOKS:
        hook.process_msg(msg)


def error_hooks(msg: str) -> None:
    for hook in ERROR_HOOKS:
        hook.process_msg(msg)


def register_hook(level: int, hookClassStr: str) -> None:
    modulePath, hookName = re.search("(.*)\.(.*)", hookClassStr).groups()
    hook = getattr(import_module(modulePath), hookName)()
    if not isinstance(hook, IHook):
        raise Exception("hook must implements from logor.interface.IHook")
    if level >= ERROR:
        ERROR_HOOKS.append(hook)
    elif level > WARNING:
        WARNING_HOOKS.append(hook)
    elif level > INFO:
        INFO_HOOKS.append(hook)
    elif level > DEBUG:
        DEBUG_HOOKS.append(hook)
    else:
        BASIC_HOOKS.append(hook)
