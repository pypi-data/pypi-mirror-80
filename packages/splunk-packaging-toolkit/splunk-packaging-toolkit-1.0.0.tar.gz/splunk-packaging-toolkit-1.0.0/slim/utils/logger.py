#!/usr/bin/env python
# coding=utf-8
#
# Copyright © Splunk, Inc. All Rights Reserved.

from __future__ import absolute_import, division, print_function, unicode_literals

from traceback import format_tb
import logging
import sys

from . internal import string
from . public import SlimEnum

__all__ = ['SlimLogger', 'SlimLoggerLevel', 'SlimExternalFormatter', 'logging_level']


SlimLoggerLevel = SlimEnum(['DEBUG', 'STEP', 'NOTE', 'WARN', 'ERROR', 'FATAL'])

logging.NOTE = logging.INFO
logging.addLevelName(logging.NOTE, 'NOTE')

logging.STEP = logging.INFO - 1
logging.addLevelName(logging.STEP, 'STEP')


def logging_level(key):
    try:
        return getattr(SlimLoggerLevel, key.upper())
    except AttributeError:
        return SlimLoggerLevel.NOTE


class SlimFormatter(logging.Formatter):
    """
    Format CLI messages to include the level name prefix strings we want
    For example, <command>: <level_name> <message + args>
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, formatstr):
        logging.Formatter.__init__(self, formatstr)

    def format(self, record):
        record.levelname = SlimFormatter._level_names.get(record.levelno, ' ')
        record.msg = '%s' * len(record.args)
        return logging.Formatter.format(self, record)

    _level_names = {
        logging.DEBUG: ' [DEBUG] ',
        logging.NOTE:  ' [NOTE] ',
        logging.WARN:  ' [WARNING] ',
        logging.ERROR: ' [ERROR] ',
        logging.FATAL: ' [FATAL] '
    }


class SlimExternalFormatter(logging.Formatter):
    """
    Provide a formatter for clients of the API to use, which does not use the
    same formatting at the CLI output (for raw message + args output)
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, formatstr):
        logging.Formatter.__init__(self, formatstr)

    def format(self, record):
        record.msg = '%s' * len(record.args)
        return logging.Formatter.format(self, record)


class SlimLogger(object):
    """
    All SLIM logging, configuration, and tracking is routed through the SlimLogger
    """

    # region Logging and logging count methods

    @classmethod
    def debug(cls, *args):
        cls._emit(SlimLoggerLevel.DEBUG, *args)

    @classmethod
    def error(cls, *args):
        cls._emit(SlimLoggerLevel.ERROR, *args)

    @classmethod
    def error_count(cls):
        return cls._message_count[SlimLoggerLevel.ERROR]

    @classmethod
    def fatal(cls, *args, **kwargs):

        exception_info = kwargs.get('exception_info')

        if exception_info is None:
            cls._emit(SlimLoggerLevel.FATAL, *args)
        else:
            error_type, error_value, traceback = exception_info

            message = string(error_type.__name__ if error_value is None else error_value)

            if cls._debug:
                message += '\nTraceback: ' + error_type.__name__ + '\n' + ''.join(format_tb(traceback))

            cls._emit(SlimLoggerLevel.FATAL, *(args + (': ', message)) if len(args) > 0 else message)

        sys.exit(1)

    @classmethod
    def information(cls, *args):
        cls._emit(SlimLoggerLevel.NOTE, *args)

    @classmethod
    def step(cls, *args):
        cls._emit(SlimLoggerLevel.STEP, *args)

    @classmethod
    def warning(cls, *args):
        cls._emit(SlimLoggerLevel.WARN, *args)

    @classmethod
    def message(cls, level, *args, **kwargs):
        if level != SlimLoggerLevel.FATAL:
            cls._emit(level, *args)
            return
        cls.fatal(*args, **kwargs)

    @classmethod
    def reset_counts(cls):
        for level in cls._message_count:
            cls._message_count[level] = 0

    @classmethod
    def exit_on_error(cls):
        if cls._message_count[SlimLoggerLevel.ERROR]:
            sys.exit(1)

    # endregion

    # region Logging configuration methods

    @classmethod
    def set_debug(cls, value):
        cls._debug = bool(value)

    @classmethod
    def is_debug_enabled(cls):
        return cls._debug is True

    @classmethod
    def set_level(cls, value):
        if isinstance(value, string):
            value = logging_level(value)
        level = cls._logging_level[value]
        cls._logger.setLevel(level)
        cls._default_level = level

    @classmethod
    def set_command_name(cls, command_name):
        cls._adapter = logging.LoggerAdapter(cls._logger, {'command_name': command_name})

    @classmethod
    def set_logger_name(cls, name):
        cls._logger.name = name

    # endregion

    # region Logging handlers

    @classmethod
    def add_handler(cls, handler):
        cls._logger.addHandler(handler)

    @classmethod
    def remove_handler(cls, handler):
        cls._logger.removeHandler(handler)

    @classmethod
    def handlers(cls):
        return cls._logger.handlers

    @classmethod
    def use_external_handler(cls, handler):
        cls.remove_handler(cls._handler)
        cls.add_handler(handler)

    # endregion

    # region Privates

    _debug = False  # turns on debug output which is different than turning on debug messages using, e.g., set_level
    _default_level = logging.STEP  # call SlimLogger.set_level to change (works in tandem with SlimLogger.set_quiet)

    _message_count = {
        SlimLoggerLevel.DEBUG: 0,
        SlimLoggerLevel.STEP:  0,
        SlimLoggerLevel.NOTE:  0,
        SlimLoggerLevel.WARN:  0,
        SlimLoggerLevel.ERROR: 0,
        SlimLoggerLevel.FATAL: 0
    }

    _logging_level = {
        SlimLoggerLevel.DEBUG: logging.DEBUG,
        SlimLoggerLevel.STEP:  logging.STEP,
        SlimLoggerLevel.NOTE:  logging.NOTE,
        SlimLoggerLevel.WARN:  logging.WARN,
        SlimLoggerLevel.ERROR: logging.ERROR,
        SlimLoggerLevel.FATAL: logging.FATAL
    }

    # noinspection PyShadowingNames
    @classmethod
    def _emit(cls, level, *args):
        cls._adapter.log(cls._logging_level[level], None, *args)
        cls._message_count[level] += 1

    @staticmethod
    def _initialize_logging():

        from os.path import basename, splitext

        command_name = splitext(basename(sys.argv[0]))[0]

        logger = logging.getLogger(command_name)
        logger.setLevel(logging.STEP)
        logger.propagate = False  # Do not try to use parent logging handlers

        handler = logging.StreamHandler()
        handler.setFormatter(SlimFormatter('%(command_name)s:%(levelname)s%(message)s'))
        logger.addHandler(handler)

        adapter = logging.LoggerAdapter(logger, {'command_name': command_name})

        return logger, handler, adapter

    _logger, _handler, _adapter = _initialize_logging.__func__()

    # endregion
    pass  # pylint: disable=unnecessary-pass
