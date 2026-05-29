"""Tests for src/myproject/utils/logger.py."""

import io
import logging
import re
import zoneinfo

import pytest

from src.myproject.utils.logger import LoggerSetup, VisualConsoleHandler, get_logger


class _TTYStream(io.StringIO):
    """StringIO that pretends to be a TTY."""

    def isatty(self):
        return True


class TestVisualConsoleHandler:
    def test_colors_applied_on_tty(self):
        stream = _TTYStream()
        handler = VisualConsoleHandler(stream=stream)
        handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
        record = logging.LogRecord(
            "test", logging.INFO, "", 0, "hello", (), None
        )
        handler.emit(record)
        output = stream.getvalue()
        assert "\033[92m" in output  # green for INFO

    def test_colors_not_applied_on_non_tty(self):
        stream = io.StringIO()
        handler = VisualConsoleHandler(stream=stream)
        record = logging.LogRecord(
            "test", logging.INFO, "", 0, "hello", (), None
        )
        handler.emit(record)
        output = stream.getvalue()
        assert "\033[" not in output

    def test_all_log_levels_have_color_mapping(self):
        expected = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "RESET"}
        assert set(VisualConsoleHandler.COLORS.keys()) == expected


class TestLoggerSetup:
    def test_creates_log_directory_and_file(self, tmp_path):
        log_dir = tmp_path / "logs"
        LoggerSetup.setup_logger("testapp", log_dir)
        assert log_dir.is_dir()
        log_files = list(log_dir.glob("testapp_*.log"))
        assert len(log_files) == 1

    def test_logger_has_two_handlers_with_file(self, tmp_path):
        logger = LoggerSetup.setup_logger("test_two", tmp_path / "logs")
        assert len(logger.handlers) == 2
        handler_types = {type(h) for h in logger.handlers}
        assert logging.FileHandler in handler_types
        assert VisualConsoleHandler in handler_types

    def test_console_only_mode_no_file(self, tmp_path):
        logger = LoggerSetup.setup_logger("test_console")
        assert len(logger.handlers) == 1
        assert isinstance(logger.handlers[0], VisualConsoleHandler)
        # No log files created anywhere
        assert list(tmp_path.glob("**/*.log")) == []

    def test_clears_handlers_on_repeat_call(self, tmp_path):
        logger1 = LoggerSetup.setup_logger("test_dup", tmp_path / "logs")
        logger2 = LoggerSetup.setup_logger("test_dup", tmp_path / "logs")
        assert logger1 is logger2  # same logger instance from logging registry
        assert len(logger2.handlers) == 2  # not 4


class TestGetLogger:
    def test_returns_configured_logger(self, tmp_path):
        logger = get_logger("test_conv", tmp_path / "logs")
        assert isinstance(logger, logging.Logger)
        assert len(logger.handlers) == 2

    def test_console_only_default(self):
        logger = get_logger("test_default")
        assert len(logger.handlers) == 1
        assert isinstance(logger.handlers[0], VisualConsoleHandler)


class TestCustomDateFormat:
    def test_custom_datefmt_applied(self, tmp_path):
        log_dir = tmp_path / "logs"
        logger = LoggerSetup.setup_logger(
            "test_fmt", log_dir, datefmt="%Y-%m-%d %H:%M:%S"
        )
        logger.info("test message")

        log_files = list(log_dir.glob("test_fmt_*.log"))
        content = log_files[0].read_text()
        # Custom format has colons in time (HH:MM:SS), military format does not
        assert re.search(r"\d{2}:\d{2}:\d{2}", content)


class TestTimezoneFallback:
    """Regression coverage for the ZoneInfoNotFoundError fallback.

    On Windows + Python 3.9+ without the `tzdata` package installed,
    ZoneInfo("America/Chicago") raises ZoneInfoNotFoundError (a KeyError
    subclass — NOT ImportError or ValueError). Before the 2026-05-29 fix,
    setup_logger would crash on import for any module that called it,
    making the project unusable on Windows without tzdata. Caught when
    heimdall-darkroom adopted the template as the first Windows downstream.
    """

    def test_setup_logger_falls_back_when_zoneinfo_data_missing(
        self, monkeypatch, tmp_path
    ):
        def boom(_name):
            raise zoneinfo.ZoneInfoNotFoundError("simulated missing tzdata")

        monkeypatch.setattr("src.myproject.utils.logger.ZoneInfo", boom)

        # Must NOT raise — the except clause should catch
        # ZoneInfoNotFoundError just like ImportError / ValueError.
        logger = LoggerSetup.setup_logger("test_tz_fallback", tmp_path / "logs")
        assert logger is not None
        assert len(logger.handlers) == 2  # file + console, fallback succeeded
