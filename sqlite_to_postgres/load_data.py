import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection

from dotenv import load_dotenv
from contextlib import contextmanager
import os
import logging
import logging.config
import time

from sqlite_extractor import SQLiteExtractor
from postgres_saver import PostgresSaver

if not os.path.exists('logs'):
    os.mkdir('logs')

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
            'datefmt': '%Y.%m.%d %H:%M:%S'
        },
    },
    'handlers': {
        'log_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': f'logs/{time.strftime("%Y-%m-%d %H:%M:%S")}.log',
            'formatter': 'default',
        },
     },
    'loggers': {
        '': {
            'handlers': ['log_file'],
            'level': 'INFO',
            'propagate': True
        },
     },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


@contextmanager
def sqlite_connection(db_path: str) -> sqlite3.Connection:
    """Контекстный менеджер для работы с SQLite"""
    conn = sqlite3.connect(db_path)
    logger.info('SQLite connection opened')
    try:
        yield conn
    except sqlite3.Error:
        logger.exception('SQLite connection error')
    finally:
        conn.close()
        logger.info('Connection to SQLite closed')


@contextmanager
def postgres_connection(dsl) -> _connection:
    """Контекстный менеджер для работы с Postgres"""
    conn = psycopg2.connect(**dsl)
    logger.info('Postgres connection opened')
    try:
        yield conn
    except psycopg2.Error:
        logger.exception('Postgres connection error')
    finally:
        conn.close()
        logger.info('Connection to Postgres closed')


def load_from_sqlite(
    connection: sqlite3.Connection,
    pg_conn: _connection
        ) -> None:
    """Основной метод загрузки данных из SQLite в Postgres"""
    sqlite_extractor = SQLiteExtractor(connection)
    postgres_saver = PostgresSaver(pg_conn)
    for table_name, table_data in sqlite_extractor.extract_pack():
        postgres_saver.save_pack(table_name, table_data)


if __name__ == '__main__':
    load_dotenv()
    dsl = {
        'dbname': os.environ.get('POSTGRES_DB'),
        'user': os.environ.get('POSTGRES_USER'),
        'password': os.environ.get('POSTGRES_PASSWORD'),
        'host': os.environ.get('POSTGRES_HOST'),
        'port': os.environ.get('POSTGRES_PORT')
    }
    with sqlite_connection(os.environ.get('DB_SQLITE_PATH')) as sqlite_conn,\
            postgres_connection(dsl) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
