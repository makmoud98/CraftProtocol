#!/usr/bin/env python

from CraftProtocol.Client.Event.HandlerPriority import HandlerPriority


def Handler(func=None, priority=HandlerPriority.NORMAL, ignore_cancelled=False):
    def _Handler_decorator(func):
        handler = func
        handler._CraftProtocol = {}

        handler._CraftProtocol["priority"] = priority
        handler._CraftProtocol["ignore_cancelled"] = ignore_cancelled

        return handler

    if callable(func):
        return _Handler_decorator(func)

    if func != None:
        raise ValueError("Please use keyword arguments")

    return _Handler_decorator
