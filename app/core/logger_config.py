import sys
from loguru import logger


def configurate_logger(level="DEBUG", log_file="app.log"):
    logger.remove()

    logger.add(
        sys.stdout,
        level="INFO",
        format="[ <g>{time:YYYY-MM-DD HH:mm:ss.SSS}</g> ] <m>{name}:{line}</m> <b><r>{level}</r></b> - <level>{message}</level>",
        colorize=True,
    )

    logger.add(
        log_file,
        level=level,
        rotation="10 MB",
        retention=10,
        compression="zip",
        format="[ {time:YYYY-MM-DD HH:mm:ss.SSS} ] {name}:{line} {level} - {message}",
        enqueue=True,
    )

    return logger
