#!/usr/bin/env python
# coding: utf-8

"""Represents buffer of uniq items. Appends item to the end if it does not exists. If buffer full,
removes first element."""

BUFFER_SIZE = 1000


class Buffer(object):
    """Buffer of uniq items.

    Args:
        size (int): buffer size
    """

    def __init__(self, size=BUFFER_SIZE):
        self.size = size
        self._buffer = []

    def append(self, i):
        """Appends item i to the end of buffer."""

        if len(self._buffer) > self.size:
            self._buffer.pop(0)
        self._buffer.append(i)

    def __contains__(self, i):
        return i in self._buffer
