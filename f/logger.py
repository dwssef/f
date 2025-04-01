import logging
import os
from typing import Optional

init_loggers = {}

DETAILED_FORMAT = '%(asctime)s - %(name)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s'
SIMPLE_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

detailed_formatter = logging.Formatter(DETAILED_FORMAT)
simple_formatter = logging.Formatter(SIMPLE_FORMAT)

DEFAULT_LEVEL = logging.DEBUG if os.getenv('LOG_LEVEL', 'INFO') == 'DEBUG' else logging.INFO

logging.basicConfig(format=SIMPLE_FORMAT, level=DEFAULT_LEVEL, force=True)

def get_logger(log_file: Optional[str] = None, log_level: int = DEFAULT_LEVEL, file_mode: str = 'w', force=False):
    """Get a logger instance that supports both console and file output.

    Args:
        log_file (str, optional): Path to the log file. If specified, logs will also be written to this file.
        log_level (int): Logging level, e.g., logging.DEBUG, logging.INFO.
        file_mode (str): File write mode, 'w' for overwrite, 'a' for append.
        force (bool): Whether to forcibly update the logger configuration (useful for reconfiguring an existing logger).
    
    Returns:
        logging.Logger: A configured logger instance.
    """

    logger_name = __name__.split('.')[0]
    logger = logging.getLogger(logger_name)
    logger.propagate = False

    if logger_name in init_loggers:
        if force:
            logger.setLevel(log_level)
            for handler in logger.handlers:
                handler.setLevel(log_level)
                handler.setFormatter(detailed_formatter if log_level == logging.DEBUG else simple_formatter)
            _add_file_handler_if_needed(logger, log_file, file_mode, log_level)
        return logger

    stream_handler = logging.StreamHandler()
    handlers = [stream_handler]

    if log_file:
        file_handler = logging.FileHandler(log_file, file_mode)
        handlers.append(file_handler)

    for handler in handlers:
        handler.setFormatter(detailed_formatter if log_level == logging.DEBUG else simple_formatter)
        handler.setLevel(log_level)
        logger.addHandler(handler)

    logger.setLevel(log_level)
    init_loggers[logger_name] = True  # 标记 logger 已初始化
    return logger

def configure_logging(debug: bool, log_file: Optional[str] = None):
    if log_file:
        get_logger(log_file=log_file, force=True)
    if debug:
        get_logger(log_level=logging.DEBUG, force=True)

def _add_file_handler_if_needed(logger, log_file, file_mode, log_level):
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            return

    if log_file:
        file_handler = logging.FileHandler(log_file, file_mode)
        file_handler.setFormatter(detailed_formatter if log_level == logging.DEBUG else simple_formatter)
        file_handler.setLevel(log_level)
        logger.addHandler(file_handler)
