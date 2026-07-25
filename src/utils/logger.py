"""
Logging utilities.
"""

import logging

from config import LOG_FORMAT, LOG_LEVEL


def setup_logger() -> None:
    """
    Configure the application logger.
    """

    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=LOG_FORMAT,
    )