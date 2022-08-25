import logging
import traceback

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def logger_raise_warn_exception(error_post_data, exception_type, detail, code=None):
    logger.warning(f'[RL]: {detail}')
    logger.warning(error_post_data)
    raise exception_type(detail=detail, code=code)


def logger_print_stacktrace(error_detail, e, error_post_data=None):
    logger.error(error_detail)
    if error_post_data is not None:
        logger.error(error_post_data)
    logger.error(e)
    logger.error(traceback.format_exc())


def logger_raise_error_exception(e, error_post_data, exception_type, detail, code=None):
    logger.error(f'[RL]: {detail}')
    logger.error(error_post_data)
    logger.error(e)
    logger.error(traceback.format_exc())
    raise exception_type(detail=detail, code=code)


def logger_info(*args):
    for info in args:
        logger.info(info)