import logging
import sys
from typing import Any

from settings.config import LOGIN, PASSWORD
from settings.strings import MSG_CREDENTIALS_ERROR, MSG_START
from worker import TestHH

logger: Any = logging.getLogger(__name__)
if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('selenium_actions.log', encoding='utf-8'),
        ],
    )
    logger.info(MSG_START)
    if LOGIN is None or PASSWORD is None:
        logger.error(MSG_CREDENTIALS_ERROR)
        raise ValueError(MSG_CREDENTIALS_ERROR)
    HH = TestHH()
    HH.run(username=LOGIN, password=PASSWORD)
