"""Async PostgreSQL database utilities with JSONB support."""

import json
import logging
from pathlib import Path

import psycopg

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages a PostgreSQL connection with a JSONB logs table."""

    def __init__(self, db_config: dict[str, str]) -> None:
        """Connect to PostgreSQL and ensure the logs table exists.

        Args:
            db_config: Connection kwargs for ``psycopg.connect``
                (user, password, host, port, dbname).
        """
        self.conn = psycopg.connect(**db_config)
        self._create_table()

    def _create_table(self) -> None:
        """Create the logs table if it doesn't exist."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS logs (
                    id SERIAL PRIMARY KEY,
                    log_name TEXT UNIQUE,
                    data JSONB
                )
                """
            )
        self.conn.commit()

    async def insert_or_update_data(self, log_name: str, data: str) -> None:
        """Insert a log entry or skip if the name already exists.

        Args:
            log_name: Unique identifier for the log entry.
            data: JSON string to store in the JSONB column.
        """
        async with self.conn.cursor() as cur:
            await cur.execute("BEGIN;")
            await cur.execute(
                "SELECT id FROM logs WHERE log_name=%s FOR UPDATE;", (log_name,)
            )
            result = await cur.fetchone()

            if result:
                logger.info("No changes detected for %s. Skipping update.", log_name)
            else:
                await cur.execute(
                    "INSERT INTO logs (log_name, data) VALUES (%s, %s);",
                    (log_name, data),
                )
                logger.info("Inserted new log: %s", log_name)

            await self.conn.commit()

    def close(self) -> None:
        """Close the database connection."""
        self.conn.close()


class LogReader:
    """Reads JSON log files from a directory and loads them into the database."""

    def __init__(self, log_dir: str | Path) -> None:
        """Initialize with the directory containing log files.

        Args:
            log_dir: Path to the directory containing .log files.
        """
        self.log_dir = Path(log_dir)

    def get_logs(self) -> list[Path]:
        """Return all .log files in the log directory."""
        return sorted(self.log_dir.glob("*.log"))

    def parse_log(self, log_file: Path) -> dict:
        """Parse a JSON log file.

        Args:
            log_file: Path to the log file.

        Returns:
            Parsed JSON as a dict.
        """
        return json.loads(log_file.read_text())

    async def process_logs(self, db_manager: DatabaseManager) -> None:
        """Read all logs and insert them into the database.

        Args:
            db_manager: Database manager instance to insert into.
        """
        for log_file in self.get_logs():
            log_name = log_file.name
            log_data = self.parse_log(log_file)
            await db_manager.insert_or_update_data(log_name, json.dumps(log_data))
