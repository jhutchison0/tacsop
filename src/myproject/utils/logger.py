"""Logging utilities with OOP setup, color output, and timezone support."""

import logging
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


class VisualConsoleHandler(logging.StreamHandler):
    """Handler that adds ANSI color to console log output."""

    COLORS: dict[str, str] = {
        "DEBUG": "\033[94m",     # Blue
        "INFO": "\033[92m",      # Green
        "WARNING": "\033[93m",   # Yellow
        "ERROR": "\033[91m",     # Red
        "CRITICAL": "\033[91m",  # Red
        "RESET": "\033[0m",
    }

    def __init__(self, stream: object = None) -> None:
        """Initialize with optional stream (defaults to sys.stderr)."""
        super().__init__(stream or sys.stderr)
        self.use_colors: bool = hasattr(self.stream, "isatty") and self.stream.isatty()

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a record with color formatting if the terminal supports it."""
        if self.use_colors:
            levelname = record.levelname
            if levelname in self.COLORS:
                record.levelname = (
                    f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
                )
        super().emit(record)


class LoggerSetup:
    """Factory for setting up loggers with consistent formatting and behavior."""

    @staticmethod
    def setup_logger(
        name: str,
        log_dir: str | Path | None = None,
        level: int = logging.INFO,
        timezone: str = "America/Chicago",
        datefmt: str | None = None,
    ) -> logging.Logger:
        """Set up a logger with file and colored console handlers.

        Args:
            name: Logger name (also used in the log filename).
            log_dir: Directory to store log files. Created if it doesn't exist.
                     None for console-only output (no file handler).
            level: Logging level (default: INFO).
            timezone: IANA timezone for timestamps (default: America/Chicago).
            datefmt: Custom date format string (default: military time "%Y-%m-%d %H%M").

        Returns:
            Configured logger instance.
        """
        if log_dir is not None:
            log_dir = Path(log_dir)
            log_dir.mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Clear existing handlers to avoid duplicate logs on re-import
        if logger.hasHandlers():
            logger.handlers.clear()

        # Resolve timezone
        try:
            tz = ZoneInfo(timezone)
            logging.Formatter.converter = lambda *args: datetime.now(tz).timetuple()
        except (ImportError, ValueError):
            tz = None
            logger.warning(
                "Could not use timezone '%s', falling back to system default",
                timezone,
            )

        # Date format: custom or military time default
        datefmt = datefmt or "%Y-%m-%d %H%M"
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt=datefmt,
        )

        # File handler with date-stamped filename
        if log_dir is not None:
            current_date = (
                datetime.now(tz).strftime("%Y%m%d")
                if tz
                else datetime.now().strftime("%Y%m%d")
            )
            file_handler = logging.FileHandler(
                log_dir / f"{name}_{current_date}.log"
            )
            file_handler.setFormatter(formatter)
            file_handler.setLevel(level)
            logger.addHandler(file_handler)

        # Console handler with color
        console_handler = VisualConsoleHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(level)
        logger.addHandler(console_handler)

        return logger


def get_logger(
    name: str,
    log_dir: str | Path | None = None,
    level: int = logging.INFO,
    timezone: str = "America/Chicago",
    datefmt: str | None = None,
) -> logging.Logger:
    """Create a configured logger with one call.

    Args:
        name: Logger name.
        log_dir: Directory for log files, or None for console-only.
        level: Logging level (default: INFO).
        timezone: IANA timezone for timestamps (default: America/Chicago).
        datefmt: Custom date format string (default: military time "%Y-%m-%d %H%M").

    Returns:
        Configured logger instance.
    """
    return LoggerSetup.setup_logger(
        name, log_dir=log_dir, level=level, timezone=timezone, datefmt=datefmt
    )
