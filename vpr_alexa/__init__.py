import logging

logger = logging.getLogger('vpr_alexa')

# Borrow Gunicorn's log formatting from https://github.com/benoitc/gunicorn/blob/2b839ca14437c61780d6eaaa8b24ad31e021f2c6/gunicorn/glogging.py
logging.basicConfig(format="%(asctime)s [%(process)d] [VPR_ALEXA] [%(levelname)s] %(message)s",
                    datefmt="[%Y-%m-%d %H:%M:%S %z]")
logger.addHandler(logging.StreamHandler())

if logger.level == logging.NOTSET:
    logger.setLevel(logging.INFO)

