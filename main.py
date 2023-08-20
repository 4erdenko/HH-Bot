import logging
import sys

from config import LOGIN, PASSWORD
from worker import TestHH

logger = logging.getLogger(__name__)
if __name__ == '__main__':
    logger.info('Start process to UP resume')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('selenium_actions.log', encoding='utf-8'),
        ],
    )

    if LOGIN is None or PASSWORD is None:
        logger.error('Cant find login and password!')
        raise ValueError('Cant find login and password!')
    HH = TestHH()
    HH.run(username=LOGIN, password=PASSWORD)
