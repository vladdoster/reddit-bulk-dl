import logging
import sys


def create_logger():
    fmt = "[%(levelname)s] %(message)s"
    _logger = logging.getLogger()
    ch = logging.StreamHandler(sys.stderr)
    ch.setFormatter(logging.Formatter(fmt))
    _logger.addHandler(ch)
    _logger.setLevel(logging.DEBUG)
    return _logger
