from contextlib import contextmanager
from typing import Tuple
import logging
import sqlite3


class SQLiteExtractor:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
        self.logger = logging.getLogger(__name__)

    @contextmanager
    def get_cursor(self) -> sqlite3.Cursor:
        """Метод для получения курсора"""
        cursor = self.connection.cursor()
        try:
            yield cursor
        except sqlite3.Error:
            self.logger.exception('Sqlite Extractor error')
        finally:
            cursor.close()

    def extract_table_names(self) -> list:
        """Метод для извлечения списка таблиц из SQLite"""
        self.logger.info('Extracting table names...')

        with self.get_cursor() as sqlite_cursor:
            sqlite_cursor.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type='table'"
            )
            tables = sqlite_cursor.fetchall()
            self.logger.info(f'Finished! Extracted {len(tables)} tables')
            return [table[0] for table in tables]

    def extract_pack(self) -> Tuple[str, list]:
        """Генератор для извлечения данных из SQLite по пакетам"""
        tables = self.extract_table_names()

        with self.get_cursor() as sqlite_cursor:
            for table in tables:
                sqlite_cursor.execute(f'PRAGMA table_info({table})')
                columns = [i[1] for i in sqlite_cursor.fetchall()]
                columns = sorted(columns)
                sqlite_cursor.execute(f'SELECT {",".join(columns)} FROM {table}')
                while True:
                    pack = sqlite_cursor.fetchmany(1000)
                    if pack:
                        self.logger.info(f'Extracted pack from {table} table')
                        yield (table, pack)
                    else:
                        break
