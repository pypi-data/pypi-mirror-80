__version__ = '6.0.1'

from zuper_commons.logs import ZLogger

logger = ZLogger(__name__)
logger.info(f'version: {__version__}')
