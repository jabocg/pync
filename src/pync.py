#!/usr/bin/env python
# Pync - Python Sync Utility
# Author: Jacob Gersztyn(@jabcog)
# 
# Prepare yourself for a boat-load of comments

# import Python 3 printing
from __future__ import print_function
# import OS specific file management library
import os
# import file comparison library
import filecmp
# import argument parsing library
import argparse
# import regex management library
import re
# import Python logging library
import logging
# import sys for standard output
import sys
# from stat import *
# import function to translate from glob to regex
from fnmatch import translate
from functools import wraps
# import shutil 
import shutil

IGNORE_FILE = '.pyncignore'

parser = argparse.ArgumentParser()
parser.add_argument("source", help="directory to sync from")
parser.add_argument("dest", help="directory to sync to")
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("-q", "--quiet", help="""suppress output, except errors,
        OVERRIDES --verbose""", action="store_true")
parser.add_argument("-n", "--no-action", help="""do NOT copy files, only print
        what would happen""", action="store_true")
COMMAND_LINE_ARGS = parser.parse_args()

handler = logging.StreamHandler(stream=sys.stdout)
formatter = logging.Formatter(
    fmt='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S%z'  # ISO8601
)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG if COMMAND_LINE_ARGS.verbose else logging.INFO)
logger.disabled = COMMAND_LINE_ARGS.quiet


def idempotent(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        # Execute function if the idempotent flag is not set.
        # Else log no action.
        logger.debug("Target function: {FUNC}".format(
            FUNC=function.__name__
            )
        )
        logger.debug("Target arguments: {ARGS}".format(
            ARGS=args
            )
        )
        logger.debug("Target keyword arguments: {KWARGS}".format(
            KWARGS=kwargs
            )
        )
        if not COMMAND_LINE_ARGS.no_action:
            function(*args, **kwargs)
        else:
            logger.info("Idempotent flag set. No action taken.")
    return wrapper


@idempotent
def makedirs(directory):
    os.makedirs(directory)


@idempotent
def copy(src, dest):
    shutil.copy2(src, dest)


def getIgnore(ignoreFile):
    home = os.path.expanduser("~")
    filepath = os.path.join(home, ignoreFile)
    logger.debug("Using {FILE}".format(FILE=filepath))
    notCommented = lambda line: not line.startswith("#")
    normalize = lambda line: translate(line.rstrip())
    with open(filepath, 'r') as ignoreFile:
        patterns = [normalize(line) for line in ignoreFile if notCommented(line)]
    for pattern in patterns:
        logger.debug("Ignoring {PATTERN}".format(PATTERN=pattern))
    return patterns


def sync(src, dest):
    patterns = getIgnore(IGNORE_FILE)
    for f in os.listdir(src):   # every file and directory in the path 'src'
        ignore = False
        matches = (re.match(pattern, f) for pattern in patterns)
        for matched in matches:
            if matched:
                logging.debug("{F} matched {PATTERN}. Ignoring".format(
                    F=f,
                    PATTERN=matched.re.pattern
                ))
                ignore = True
                break
        if not ignore:
            # Join the source and filename.
            source = os.path.join(src, f)
            logger.debug("Source: {SOURCE}".format(SOURCE=source))
            # Join the destination and filename.
            destination = os.path.join(dest, f)
            logger.debug("Destination: {DESTINATION}".format(
                DESTINATION=destination
                )
            )
            if os.path.isdir(source):  # if the current item is a directory
                logger.debug("{PATH} is a directory".format(PATH=source))
                # If the destination directory does not exist
                if not os.path.exists(destination):
                    logger.info("Creating {DESTINATION}".format(
                        DESTINATION=destination
                        )
                    )
                    makedirs(destination)
                # Recursively sync data in directory
                logger.debug("Recursing into {SOURCE}".format(
                    SOURCE=source
                    )
                )
                sync(source, destination)
            elif os.path.isfile(source):  # if the current item is a file
                # Copy to destination
                logger.info("{SOURCE} is a file".format(SOURCE=source))
                copyto(source, destination)
            else:
                # Unknown error fall through.
                logger.debug("Error: skipping {FILE}".format(FILE=source))
        else:
            logger.info("Ignoring {FILE}".format(FILE=f))


def copyto(src, dest):
    if not os.path.exists(dest):
        logger.info("{DEST} does not exist. Creating.".format(DEST=dest))
        copy(src, dest)
        logger.debug("{SRC} -> {DEST}".format(SRC=src, DEST=dest))
    else:
        logger.info("{DEST} exists.".format(DEST=dest))
        if not filecmp.cmp(src, dest):
            logger.info("{SRC} and {DEST} are not identical".format(
                SRC=src,
                DEST=dest
                )
            )
            if os.path.getctime(src) > os.path.getctime(dest):
                logger.info("{SRC} is newer than {DEST}".format(
                    SRC=src,
                    DEST=dest)
                )
                copy(src, dest)
                logger.debug("{SRC} -> {DEST}".format(SRC=src, DEST=dest))
        else:
            logger.info("{SRC} and {DEST} are identical".format(
                SRC=src,
                DEST=dest
                )
            )


def main():
    getIgnore(".pyncignore")
    sync(COMMAND_LINE_ARGS.source, COMMAND_LINE_ARGS.dest)


if __name__ == "__main__":
    main()
