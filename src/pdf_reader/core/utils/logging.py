import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(levelname)s] method: %(funcName)s: %(message)s"
)

logger = logging.getLogger(__name__)


class Logger:
    debug = staticmethod(logger.debug)
    info = staticmethod(logger.info)
    warning = staticmethod(logger.warning)
    error = staticmethod(logger.error)
    critical = staticmethod(logger.critical)