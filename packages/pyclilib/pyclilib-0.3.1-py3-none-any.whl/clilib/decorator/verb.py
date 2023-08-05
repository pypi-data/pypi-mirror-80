import clilib.util

logger = clilib.util.get_logger(f"[{__name__}]")


def verb(*args, **kwargs):
    logger.debug('Decorating verb')
    logger.debug(f"args  : {args}")
    logger.debug(f"kwargs: {kwargs}")

    func = args[0]
    logger.debug(f"func  : {func}")

    action = func.__name__
    logger.debug(f"action: {action}")
    logger.debug(f"Adding attribute '_action={action}' to decorated method")
    setattr(func, '_action', action)

    return func
