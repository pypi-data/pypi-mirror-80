# coding=utf-8
#
# Copyright © Splunk, Inc. All Rights Reserved.

from __future__ import absolute_import, division, print_function, unicode_literals


class NamedObject(object):
    __slots__ = ('_name',)

    def __init__(self, name):
        self._name = name

    def __cmp__(self, other):
        # noinspection PyProtectedMember
        return self._name.__cmp__(other._name)  # pylint: disable=protected-access

    def __hash__(self):
        return self._name.__hash__()

    @property
    def name(self):
        return self._name
