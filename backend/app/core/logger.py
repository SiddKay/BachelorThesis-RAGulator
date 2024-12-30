import json
import logging
from pathlib import Path
import sys
from datetime import datetime, timezone
from typing import Optional, override

# ==================== #
#  Logging Formatters  #
# ==================== #


class VSCodeFormatter(logging.Formatter):
    """Custom formatter with colorized level names, that creates clickable file links in VS Code terminal."""

    COLORS = {
        logging.INFO: "\033[94m",  # blue
        logging.WARNING: "\033[93m",  # yellow
        logging.ERROR: "\033[91m",  # red
        logging.CRITICAL: "\033[95m",  # pink
    }
    DARK_GRAY = "\033[90m"
    RESET = "\033[0m"

    @override
    def format(self, record: logging.LogRecord) -> str:
        """
        Format a log record with a colorized level name and a clickable file link
        to the source file in VS Code format. INFO level logs are specifically
        colored blue to distinguish them from other processes (e.g., Uvicorn's
        INFO logs are green).
        """

        # Colorize the level name
        color = self.COLORS.get(record.levelno, "")
        levelname_colorised = f"{color}{record.levelname}{self.RESET}"

        # Get the full file path
        file_path = Path(record.pathname).resolve()

        # Create VS Code clickable link format: file:line:column with surrounding gray color
        file_link = f"{file_path}:{record.lineno}:1"
        file_info = f"{self.DARK_GRAY}{file_link} [{record.module}:{record.funcName}]{self.RESET}"

        # Final format
        return (
            f"{levelname_colorised}:     {file_info} - {record.getMessage()}"
        )


class JsonFormatter(logging.Formatter):
    """JSON formatter for file logging."""

    def __init__(self):
        super().__init__()
        self.default_msec_format = "%s.%03d"

    @override
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON with additional context."""
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
            "process": record.process,
        }

        # Add extra fields if they exist
        if hasattr(record, "extra"):
            log_data.update(record.extra)

        if record.exc_info:
            log_data["exc_info"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


# =============== #
#  Logging Setup  #
# =============== #


def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[str | Path] = None,
) -> None:
    """Initialize logging with console and optional file output."""
    # Clear existing handlers
    root = logging.getLogger()
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)

    handlers: list[logging.Handler] = []

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(level)
    console.setFormatter(VSCodeFormatter())
    handlers.append(console)

    # File handler
    if log_file:
        log_path = Path(log_file)
        log_dir = log_path.parent
        log_name = log_path.stem  # Get name without extension

        # Create logs directory if it doesn't exist
        log_dir.mkdir(parents=True, exist_ok=True)

        file_handler = logging.handlers.RotatingFileHandler(
            filename=str(log_dir / f"{log_name}.jsonl"),
            maxBytes=256 * 1024,  # 256KB
            backupCount=5,
            encoding="utf8",
        )

        # Override the default rotation naming pattern
        @override
        def namer(default_name: str) -> str:
            """Generate backup filename while preserving .jsonl extension."""
            # Extract the rotation number from the default name
            base_path = Path(default_name)
            if base_path.suffix.startswith("."):
                rotation_num = base_path.suffix[1:]  # Remove the leading dot
                if rotation_num.isdigit():
                    # Construct new name: basename.{number}.jsonl
                    return str(log_dir / f"{log_name}{rotation_num}.jsonl")
            return default_name

        file_handler.namer = namer
        file_handler.setFormatter(JsonFormatter())
        file_handler.setLevel(logging.DEBUG)
        handlers.append(file_handler)

    # Configure root logger
    logging.basicConfig(level=level, handlers=handlers, force=True)


def get_logger(name: str = "ragulator_logger") -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
