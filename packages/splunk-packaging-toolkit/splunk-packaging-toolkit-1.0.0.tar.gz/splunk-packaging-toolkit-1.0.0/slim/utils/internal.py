#!/usr/bin/env python
# coding=utf-8
#
# Copyright © Splunk, Inc. All Rights Reserved.

from __future__ import absolute_import, division, print_function, unicode_literals

from hashlib import sha1
from os import path
from sys import getdefaultencoding, version_info

import io


if version_info.major >= 3:
    # noinspection PyShadowingBuiltins
    long = int    # pylint: disable=redefined-builtin, invalid-name
    char = chr
    string = str  # pylint: disable=invalid-name
else:
    # noinspection PyCompatibility
    if getdefaultencoding() != 'utf-8':  # TODO: remove this when we've got a virtualenv setup
        import sys
        # noinspection PyCompatibility
        reload(sys)
        # noinspection PyUnresolvedReferences
        sys.setdefaultencoding('utf-8')  # pylint: disable=no-member
        # noinspection PyUnresolvedReferences
        del sys.setdefaultencoding       # pylint: disable=no-member

    del getdefaultencoding

    # noinspection PyShadowingBuiltins,PyUnboundLocalVariable
    long = long       # pylint: disable=redefined-builtin, invalid-name
    char = unichr
    string = unicode  # pylint: disable=invalid-name
    # noinspection PyCompatibility
    from future_builtins import filter, map  # pylint: disable=redefined-builtin, unused-import


def hash_object(filename, size=-1):
    """
    Computes an object ID from a file the way Git does. [1]_

    :param filename: Path to file.
    :type filename: string
    :param size: Length of file.
    :return: Object ID.
    :rtype: string

    .. rubric:: Footnotes
    .. [1] `Git Tip of the Week: Objects <http://goo.gl/rvfWtM>`

    """
    if size == -1:
        size = path.getsize(filename)
    object_id = sha1()
    object_id.update(b'blob ' + bytes(size) + b'\0')
    if size > 0:
        with io.open(filename, 'rb') as istream:
            block = bytearray(65535)
            while True:
                length = istream.readinto(block)
                if length == 0:
                    break
                object_id.update(block[:length])
    return string(object_id.hexdigest())
