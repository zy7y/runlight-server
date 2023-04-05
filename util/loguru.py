import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(levelname)s %(asctime)s [%(filename)s:%(lineno)d] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "default"},
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "app.log",
            "maxBytes": 10485760,
            "backupCount": 10,
            "formatter": "default",
            "encoding": "utf8",
        },
    },
    "root": {"level": "DEBUG", "handlers": ["console", "file"]},
}

# 将配置应用于 logging 模块
logging.config.dictConfig(LOGGING_CONFIG)

LOG = logging.getLogger(__name__)
