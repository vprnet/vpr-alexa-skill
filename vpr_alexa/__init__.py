import logging

logger = logging.getLogger('vpr_alexa')
logger.addHandler(logging.StreamHandler())
if logger.level == logging.NOTSET:
    logger.setLevel(logging.WARN)

