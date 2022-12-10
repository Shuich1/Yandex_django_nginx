from psycopg2.extensions import connection as _connection
import psycopg2

import logging


class PostgresSaver:
    def __init__(self, connection: _connection):
        self.connection = connection
        self.logger = logging.getLogger(__name__)

    def save_pack(self, table_name: str, pack: list) -> None:
        """Метод для сохранения данных в Postgres"""
        self.logger.info(f'Saving {table_name} pack...')
        with self.connection.cursor() as pg_cursor:
            query = ','.join(
                pg_cursor.mogrify(
                    f'({",".join(["%s"] * len(row))})',
                    row
                ).decode('utf-8') for row in pack
            )
            try:
                pg_cursor.execute('SELECT column_name FROM information_schema.columns '
                                  f'WHERE table_name = \'{table_name}\';')
                columns = pg_cursor.fetchall()
                columns = [column[0] for column in columns]
                columns = sorted(columns)

                pg_cursor.execute(
                    f'INSERT INTO content.{table_name} ({",".join(columns)}) '
                    f'VALUES {query} ON CONFLICT DO NOTHING'
                )
                self.logger.info(f'Pack {table_name} saved')
            except psycopg2.Error:
                self.logger.exception(
                    f'Not saved {table_name} pack from '
                    f'{pack[0][0]} to {pack[-1][0]}'
                )
            finally:
                self.connection.commit()
