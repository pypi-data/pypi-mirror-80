import re
import logging

import argparse
from pylogrus import PyLogrus, TextFormatter

_log_level = logging.INFO


# https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
def to_kebab(word):
    word = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', word)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', word).lower()


def get_logger(name=__name__):
    logging.setLoggerClass(PyLogrus)
    logger = logging.getLogger(name)
    logger.setLevel(_log_level)

    formatter = TextFormatter(datefmt='Z', colorize=True)

    ch = logging.StreamHandler()
    ch.setLevel(_log_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger.withPrefix(name)


def get_subparser(parser):
    # Couldn't find a function in argparse to do this
    # It's already stored in the parser object. Doesn't make sense to have another mapping for it
    for action in parser.__dict__['_actions']:
        if (type(action) is argparse._SubParsersAction):
            return action

    subparser = parser.add_subparsers(dest='_cmd')
    subparser.required = True

    return subparser
