import clilib.util
import clilib.decorator.util


logger = clilib.util.get_logger(f"[{__name__}]")


def resource(klass):
    logger.debug(f"class: {klass}")

    logger.debug("Adding attributes '_parsers' and '_name'")
    setattr(klass, '_parsers', {})
    setattr(klass, '_name', '')

    logger.debug(f"Finding verb decorated functions in {klass}")
    for key, value in klass.__dict__.items():
        logger.debug(f"Checking {key}")
        if callable(value) and clilib.decorator.util.is_verb(value):
            logger.debug(f"{key} is decorated!")
            clilib.register_verb(klass, value)

            if hasattr(value, '_args'):
                logger.debug('Adding args')

    return klass
