import json
import logging
from pathlib import Path
import sys
from datetime import datetime, timezone
from typing import Optional, override

# ==================== #
#  Logging Formatters  #
# ==================== #


class ConsoleFormatter(logging.Formatter):
    """Simple console formatter with colors."""

    COLORS = {
        logging.INFO: "\033[92m",  # green
        logging.WARNING: "\033[93m",  # yellow
        logging.ERROR: "\033[91m",  # red
        logging.CRITICAL: "\033[95m",  # pink
    }
    BLUE = "\033[94m"  # for exceptions
    RESET = "\033[0m"

    @override
    def format(self, record: logging.LogRecord) -> str:
        # Create a copy of the record to avoid modifying the original
        record_copy = logging.makeLogRecord(record.__dict__)

        # Choose blue for exceptions, otherwise use level color
        if record_copy.exc_info:
            color = self.BLUE
        else:
            color = self.COLORS.get(record_copy.levelno, "")

        record_copy.levelname = f"{color}{record_copy.levelname}{self.RESET}"

        return super().format(record_copy)


class JsonFormatter(logging.Formatter):
    """JSON formatter for file logging."""

    @override
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "level": record.levelname,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "thread_name": record.threadName,
            "logger": record.name,
        }

        if record.exc_info:
            log_data["exc_info"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


# =============== #
#  Logging Setup  #
# =============== #


def setup_logging(
    level: int = logging.DEBUG, log_file: Optional[str | Path] = None
) -> None:
    """Initialize logging with console and optional file output.

    Args:
        level: Minimum logging level
        log_file: Optional path to log file
    """
    handlers: list[logging.Handler] = []

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(
        ConsoleFormatter(
            "%(levelname)s @ %(module)s:%(funcName)s:%(lineno)d - %(message)s"
        )
    )
    handlers.append(console)

    # File handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_path,
            maxBytes=512 * 1024,  # 512KB
            backupCount=3,
            encoding="utf8",
        )
        file_handler.setFormatter(JsonFormatter())
        handlers.append(file_handler)

    # Configure root logger
    logging.basicConfig(level=level, handlers=handlers, force=True)


def get_logger(name: str = "ragulator_logger") -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
