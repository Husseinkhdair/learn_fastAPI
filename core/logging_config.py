import logging 
import os
from contextvars import ContextVar

correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="-")


class CorrelationIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.correlation_id = correlation_id_var.get()
        return True


def setup_logging():
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    # Show logs in console or terminal
    console_handler = logging.StreamHandler()

    # Create a file handler to write logs to a file
    file_handler = logging.FileHandler(
        "logs/app.log",
        encoding="utf-8"
    )

    # -------------------------
    # Correlation ID
    # -------------------------
    correlation_filter = CorrelationIdFilter()
    console_handler.addFilter(correlation_filter)
    file_handler.addFilter(correlation_filter)

    # -------------------------
    # Log Format
    # -------------------------
    formatter = logging.Formatter(
        "%(asctime)s | "
        "%(levelname)s | "
        "correlation_id=%(correlation_id)s | "
        "%(name)s | "
        "%(message)s"
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # -------------------------
    # Root Logger
    # -------------------------
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Remove old handlers
    root_logger.handlers.clear()

    # Add handlers
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
