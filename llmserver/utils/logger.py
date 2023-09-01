from logging import Logger, getLogger

logger: Logger = getLogger()


def info(tag, msg):
    logger.info(f"{tag}:{msg}")


def error(tag, msg):
    logger.error(f"{tag}:{msg}")


def warn(tag, msg):
    logger.warning(f"{tag}:{msg}")
