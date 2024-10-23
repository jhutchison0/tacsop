# -*- coding: utf-8 -*-
"""
Created on Tue Feb 07 11:00:00 2023

@author: jhutchison


mamba install conda-forge::psycopg
"""

# %% Packages
""" Third party and local imports """

import pathlib
import psycopg
import asyncio
import os
import json

# %% Functions
""" Define functions """


class DatabaseManager:
    def __init__(self, db_config):
        self.conn = psycopg.connect(**db_config)
        self.create_table()

    def create_table(self):
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

    async def insert_or_update_data(self, log_name, data):
        async with self.conn.cursor() as cur:
            await cur.execute("BEGIN;")
            await cur.execute(
                "SELECT id FROM logs WHERE log_name=%s FOR UPDATE;", (log_name,)
            )
            result = await cur.fetchone()

            if result:
                print(f"No changes detected for {log_name}. Skipping update.")
            else:
                await cur.execute(
                    "INSERT INTO logs (log_name, data) VALUES (%s, %s);",
                    (log_name, data),
                )
                print(f"Inserted new log: {log_name}")

            await self.conn.commit()

    def close(self):
        self.conn.close()


class LogReader:
    def __init__(self, log_dir):
        self.log_dir = log_dir

    def get_logs(self):
        return [
            os.path.join(self.log_dir, f)
            for f in os.listdir(self.log_dir)
            if f.endswith(".log")
        ]

    def parse_log(self, log_file):
        with open(log_file, "r") as f:
            data = f.read()
        return json.loads(data)

    async def process_logs(self, db_manager):
        logs = self.get_logs()
        for log_file in logs:
            log_name = os.path.basename(log_file)
            log_data = self.parse_log(log_file)
            await db_manager.insert_or_update_data(log_name, json.dumps(log_data))


# %% Variables
""" Set script (global) variables """

path_data = pathlib.Path("data/")


# %% Main
""" Display task data """

if __name__ == "__main__":
    log_dir = "/path/to/logs"  # Replace with your log directory
    db_config = {
        "user": "your_user",
        "password": "your_password",
        "host": "your_host",
        "port": "5432",
        "dbname": "your_dbname",
    }

    db_manager = DatabaseManager(db_config)
    log_reader = LogReader(log_dir)

    asyncio.run(log_reader.process_logs(db_manager))
    db_manager.close()
