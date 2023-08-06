"""
Basic test of the SL10
"""
import time
import logging
from prosonix.sonolab import SL10
from prosonix.errors import SonolabError, SL10OverError


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    port = 'COM6'
    sl10 = SL10(port)
    sl10.on()
    sl10.power(10)
    time.sleep(2)
    p = sl10.power()
    if 9 <= p <= 11:
        logger.info('Power set successfully to 10')
    else:
        logger.warning('Power failed to be set to 6, add some more time between setting and reading power. Otherwise, '
                       'there might be some other problem')
    sl10.power(6)
    time.sleep(2)
    p = sl10.power()
    if 5 <= p <= 7:
        logger.info('Power set successfully to 6')
    else:
        logger.warning('Power failed to be set to 6, add some more time between setting and reading power. Otherwise, '
                       'there might be some other problem')
    try:
        sl10.power(1000)
    except SL10OverError:
        logger.info('Caught over error to set power to 1000 successfully')
    try:
        sl10.power(5)
    except SL10OverError:
        logger.info('Caught over error to set power to 5 successfully')
    sl10.off()
    sl10.disconnect()
