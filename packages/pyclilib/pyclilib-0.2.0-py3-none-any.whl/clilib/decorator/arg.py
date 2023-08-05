import clilib.util


logger = clilib.util.get_logger(f"[{__name__}]")


def arg(*decorator_args, **decorator_kwargs):
    logger.debug('Handling @arg decorator')
    logger.debug(f"args  : {decorator_args}")
    logger.debug(f"kwargs: {decorator_kwargs}")

    def wrapper(func):
        logger.debug(f"@arg is wrapping: {func}")

        if not hasattr(func, '_args'):
            logger.debug('_args attribute not found, setting as []')
            setattr(func, '_args', [])

        logger.debug('Retrieving _args attribute')
        _args = getattr(func, '_args')

        logger.debug(f"Appending to _args: ({decorator_args}, {decorator_kwargs})")
        _args.append((decorator_args, decorator_kwargs))

        return func

    return wrapper
