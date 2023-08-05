import logging
import os


def logger(package):
    logger = logging.getLogger(package)
    logfile = os.path.join(os.environ('SYSTEMROOT'), 'WAPT', 'logs', package + '.log')
    os.makedirs(os.path.dirname(logfile))

    logger.basicConfig(
        filename=logfile,
        format='%(asctime)s %(levelname)s %(funcName)s: %(message)s',
        level=logging.DEBUG)

    return logger
