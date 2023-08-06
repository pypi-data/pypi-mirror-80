#!/usr/bin/env python
# coding=utf-8
#
# Copyright © Splunk, Inc. All Rights Reserved.

from __future__ import absolute_import, division, print_function, unicode_literals

from os import path
import sys

from slim.utils import *
from slim.app import *
from slim.command import *


# Argument parser definition

parser = SlimArgumentParser(
    description='create a new or updated app manifest',
    epilog='The manifest created is based on the app\'s configuration settings.'
)

parser.add_app_directory()
parser.add_argument_help()
parser.add_output_file(description='app manifest')

# Command-specific arguments

parser.add_argument(
    '--update', dest='update', action='store_true', help='amend the current app manifest based on configuration '
    'settings.'
)


def main(args):

    if args.update is True:
        update_manifest(args.source, args.output)
    else:
        generate_manifest(args.source, args.output)


def generate_manifest(source, output, add_defaults=True):

    SlimLogger.step('Parsing app configuration at ', encode_filename(source), '...')
    app_configuration = AppConfiguration.load(source)
    SlimLogger.exit_on_error()

    SlimLogger.step('Generating app manifest to ', encode_filename(output.name), '...')
    AppManifest.generate(app_configuration, output, add_defaults)
    SlimLogger.exit_on_error()

    SlimLogger.information('App manifest saved to ', encode_filename(output.name))


def update_manifest(source, output):

    app_manifest_filename = path.join(source, 'app.manifest')

    if not path.isfile(app_manifest_filename):
        generate_manifest(source, output)
        return

    SlimLogger.step('Parsing app configuration at ', encode_filename(source), '...')
    app_configuration = AppConfiguration.load(source)
    SlimLogger.exit_on_error()

    SlimLogger.step('Loading app manifest from ', encode_filename(app_manifest_filename), '...')
    app_manifest = AppManifest.load(app_manifest_filename)
    SlimLogger.exit_on_error()

    SlimLogger.step('Updating app manifest from app configuration to ', encode_filename(output.name), '...')
    app_manifest.amend(app_configuration)
    SlimLogger.exit_on_error()

    with output:
        app_manifest.save(output, indent=True)

    SlimLogger.information('App manifest saved to ', encode_filename(output.name))


if __name__ == '__main__':
    # noinspection PyBroadException
    try:
        main(parser.parse_args(sys.argv[1:]))
    except SystemExit:
        raise
    except:
        SlimLogger.fatal(exception_info=sys.exc_info())
