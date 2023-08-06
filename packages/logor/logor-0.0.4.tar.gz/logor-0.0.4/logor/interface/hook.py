# coding: utf-8
__all__ = "IHook",


class IHookMetaClass(type):

    def __new__(cls, name: str, bases: tuple, attrs: dict):
        if bases:
            if IHook not in bases:
                raise Exception(f"please ensure `{name}` implemented the interface of `logor.interface.IHook`")
            if "process_msg" not in attrs:
                raise Exception(f"please ensure `{name}` implemented the function of `process_msg`")
        return type.__new__(cls, name, bases, attrs)


class IHook(metaclass=IHookMetaClass):

    def process_msg(self, msg: str) -> None:
        raise NotImplementedError
