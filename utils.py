import time
import logging
from functools import wraps

logger_ = logging.getLogger(__name__)


def error_handler_old(exception_to_check, tries=5, delay=1, backoff=2, logger=logger_):
    """Retry calling the decorated function using an exponential backoff;
    :param exception_to_check: the exception to check. may be a tuple of
        exceptions to check
    :type exception_to_check: Type[Exception]
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use.
    :type logger: logging.Logger instance
    """

    def deco_retry(f):

        @wraps(f)
        def func_retry(*args, **kwargs):
            m_tries, m_delay = tries, delay
            while m_tries > 1:
                try:
                    return f(*args, **kwargs)
                except exception_to_check as e:
                    msg = f"{e}, Retrying in {m_delay} seconds..."
                    logger.warning(msg)
                    time.sleep(m_delay)
                    m_tries -= 1
                    m_delay *= backoff
            return f(*args, **kwargs)

        return func_retry

    return deco_retry


def error_handler(exception_to_check, tries=5, delay=1, backoff=2, driver_delay=0.5, logger=logger_):
    """Retry calling the decorated function using an exponential backoff;
    :param exception_to_check: the exception to check. may be a tuple of
        exceptions to check
    :type exception_to_check: Type[Exception]
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param driver_delay: number of times driver delay
    :type driver_delay: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use.
    :type logger: logging.Logger instance
    """

    def deco_retry(f):

        @wraps(f)
        def func_retry(*args, **kwargs):
            m_tries, m_delay, d_delay = tries, delay, driver_delay
            while m_tries > 1:
                try:
                    return f(*args, **dict(kwargs, wait=d_delay))
                except exception_to_check as e:
                    msg = f"{e}, Retrying in {m_delay} seconds..."
                    logger.warning(msg)
                    time.sleep(m_delay)
                    m_tries -= 1
                    m_delay *= backoff
                    d_delay *= backoff
            return f(*args, **dict(kwargs, wait=d_delay))

        return func_retry

    return deco_retry


# Use case example
@error_handler(Exception, tries=4)
def test_fail(text):
    print(text)
    raise Exception("Some error")


if __name__ == "__main__":
    test_fail("it works!")
