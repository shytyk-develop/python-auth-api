import logging
from logging.config import dictConfig


def configure_logging() -> None:
    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"default": {"format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s"}},
        "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "default"}},
        "root": {"handlers": ["console"], "level": "INFO"},
        "loggers": {
            "uvicorn": {"handlers": ["console"], "level": "INFO", "propagate": False},
            "uvicorn.error": {"handlers": ["console"], "level": "INFO", "propagate": False},
            "uvicorn.access": {"handlers": ["console"], "level": "INFO", "propagate": False},
        },
    })
    logging.getLogger(__name__).info("Logging configured")
