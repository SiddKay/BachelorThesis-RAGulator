import json
import logging
import atexit
import pathlib
import logging.config
import datetime as dt
from typing import Optional, override

# =============== #
#  Logging Setup  #
# =============== #


class LoggingManager:
    """Manages logging configuration and initialization for the application."""

    def __init__(
        self,
        config_path: Optional[str | pathlib.Path] = None,
        logs_dir: Optional[str | pathlib.Path] = None,
    ):
        """
        Initialize the logging manager.

        Args:
            config_path: Path to logging config JSON file. If None, uses default path.
            logs_dir: Path to logs directory. If None, uses default path.
        """
        self.backend_dir = pathlib.Path(__file__).parent.parent.parent
        self.config_path = (
            pathlib.Path(config_path)
            if config_path
            else self.backend_dir / "src" / "configs" / "logging_config.json"
        )
        self.logs_dir = (
            pathlib.Path(logs_dir) if logs_dir else self.backend_dir / "logs"
        )

    def setup(self) -> None:
        """Set up logging configuration with directory creation and error handling."""

        try:
            self._ensure_logs_directory()
            config = self._load_config()
            logging.config.dictConfig(config)

            # Start queue handler listener if present
            queue_handler = logging.getHandlerByName("queue_handler")

            if queue_handler is not None:
                # print(queue_handler)
                queue_handler.listener.start()
                atexit.register(queue_handler.listener.stop)

        except Exception as e:
            # Fall back to basic logging if setup fails
            logging.basicConfig(
                level=logging.INFO, format="%(levelname)s: %(message)s"
            )
            logging.error(f"Failed to configure logging: {str(e)}")
            logging.warning("Falling back to basic logging configuration")

    def _ensure_logs_directory(self) -> None:
        """Create logs directory if it doesn't exist."""
        self.logs_dir.mkdir(parents=True, exist_ok=True)

    def _load_config(self) -> dict:
        """Load logging configuration from JSON file."""
        try:
            with open(self.config_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Logging configuration file not found at {self.config_path}"
            )


def get_logger(name: str = "ragulator_logger") -> logging.Logger:
    """Get a logger instance with the specified name."""
    return logging.getLogger(name)


# ==================== #
#  Logging Formatters  #
# ==================== #

LOG_RECORD_BUILTIN_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
}


class CustomJSONFormatter(logging.Formatter):
    def __init__(
        self,
        *,
        fmt_keys: dict[str, str] | None = None,
    ):
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    @override
    def format(self, record: logging.LogRecord) -> str:
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def _prepare_log_dict(self, record: logging.LogRecord):
        always_fields = {
            "message": record.getMessage(),
            "timestamp": dt.datetime.fromtimestamp(
                record.created, tz=dt.timezone.utc
            ).isoformat(),
        }
        if record.exc_info is not None:
            always_fields["exc_info"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            always_fields["stack_info"] = self.formatStack(record.stack_info)

        message = {
            key: (
                msg_val
                if (msg_val := always_fields.pop(val, None)) is not None
                else getattr(record, val)
            )
            for key, val in self.fmt_keys.items()
        }
        message.update(always_fields)

        for key, val in record.__dict__.items():
            if key not in LOG_RECORD_BUILTIN_ATTRS:
                message[key] = val

        return message


class NonErrorFilter(logging.Filter):
    @override
    def filter(self, record: logging.LogRecord) -> bool | logging.LogRecord:
        return record.levelno <= logging.INFO
