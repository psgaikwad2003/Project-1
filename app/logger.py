"""Structured JSON logging configuration for enterprise observability."""

import json
import logging
import sys
from datetime import datetime, timezone
from app.config import get_settings


class JSONFormatter(logging.Formatter):
    """Custom formatter outputting logs as JSON lines for log aggregators (ELK, FluentBit, Loki)."""

    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "line": record.lineno,
        }
        if hasattr(record, "correlation_id"):
            log_record["correlation_id"] = record.correlation_id
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


def setup_logger(name: str = "cloudops-nexus") -> logging.Logger:
    """Initialize and configure root application logger."""
    settings = get_settings()
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL.upper())

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)

    return logger
