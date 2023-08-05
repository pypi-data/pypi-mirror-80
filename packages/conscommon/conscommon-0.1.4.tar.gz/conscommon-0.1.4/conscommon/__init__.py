__version__ = "0.1.4"
__author__ = "Carneiro, Claudio F."

import logging
from typing import Optional, List


def get_logger(
    name=__file__,
    level: int = logging.WARNING,
    handlers: Optional[List[logging.Handler]] = None,
) -> logging.Logger:
    """ Returns a logger object """

    logger = logging.getLogger(name)

    if not len(logger.handlers) and not handlers:
        formatter = logging.Formatter("%(name)s [%(levelname)s] %(message)s")
        logger.setLevel(level)
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
    return logger
