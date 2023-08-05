import clilib.util
import clilib.decorator as decorator
import argparse
import logging


_root_parser = argparse.ArgumentParser()
_subparsers = _root_parser.add_subparsers(dest='_cmd')
_subparsers.required = True
_args = None

logger = clilib.util.get_logger(f"[{__name__}]")


def build_parser(parser):
    return parser


def register_verb(resource, func):
    logger.debug('Registering resource verb')
    logger.debug(_subparsers.choices)

    resource_name = clilib.util.to_kebab(resource.__name__)
    verb = getattr(func, '_action')
    args = getattr(func, '_args', []) + getattr(resource, '_args', [])

    logger.debug(f"resource: {resource}")
    logger.debug(f"func    : {func}")
    logger.debug(f"verb    : {verb}")
    logger.debug(f"args    : {args}")

    if verb not in _subparsers.choices:
        logger.debug(f"Adding verb, '{verb}', in _subparsers")
        _subparsers.add_parser(verb)

    if verb not in resource._parsers:
        logger.debug(f"Adding verb, '{verb}', in resource._parsers")
        if verb in _subparsers.choices:
            logger.debug(f"Referencing subparser of _subparsers.choices['{verb}']")
            resource._parsers[verb] = clilib.util.get_subparser(_subparsers.choices[verb])
        else:
            logger.debug(f"Creating _subparsers.choices['{verb}']")
            resource._parsers[verb] = _subparsers.choices[verb].add_subparsers()

    logger.debug(resource._parsers[verb].choices)
    if resource_name not in resource._parsers[verb].choices:
        logger.debug(f"Adding resource, {resource}, target for verb, {verb}, as {resource_name}")
        resource_parser = resource._parsers[verb].add_parser(resource_name)
        resource_parser.set_defaults(_func=func, _klass=resource)

        for arg in args:
            rargs, rkwargs = arg

            logger.debug(f"Adding arg to '{verb} {resource_name}': {rargs}, {rkwargs}")
            resource_parser.add_argument(*rargs, **rkwargs)


def init(prog):
    global _root_parser

    _root_parser.prog = prog


def run(prog):
    global _root_parser
    global _args
    global _subparsers

    _root_parser.prog = prog
    _args = _root_parser.parse_args()

    if hasattr(_args, '_func'):
        _args._func(_args._klass, args=_args)
