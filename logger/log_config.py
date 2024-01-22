log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "./Logs/app.log",
            "maxBytes": 10000,
            "backupCount": 3,
        },
    },
    "loggers": {
        "logger_remcomender": {"handlers": ["default"], "level": "INFO"},
    },
}
