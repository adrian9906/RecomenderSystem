import logging
from logging.config import dictConfig
from .log_config import log_config
# Disable uvicorn access logger

def log_app():    
    dictConfig(log_config)
    logger = logging.getLogger("logger_remcomender")
    logger.setLevel(logging.getLevelName(logging.DEBUG))
    return logger