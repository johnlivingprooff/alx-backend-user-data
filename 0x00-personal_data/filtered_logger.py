#!/usr/bin/env python3
"""returns the log message obfuscated:"""
import mysql.connector
import re
import logging
import os
from mysql.connector.connection import MySQLConnection
from typing import List, Tuple
from logging import Logger


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    return re.sub(f'({"|".join(fields)})=[^{separator}]*',
                  lambda m: f'{m.group().split("=")[0]}={redaction}', message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Tuple[str]) -> None:
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super().format(record)


PII_FIELDS: Tuple[str] = ('name', 'email', 'phone', 'ssn', 'password')


def get_logger() -> Logger:
    """Returns a logging.Logger object configured for user data"""
    logger: Logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def main() -> None:
    """Main function that retrieves and logs user data from the database"""
    logger: Logger = get_logger()

    try:
        db: MySQLConnection = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")

        for row in cursor:
            msg = "; ".join(f"{key}={value}" for key, value in row.items())
            logger.info(msg)

        cursor.close()
        db.close()
    except mysql.connector.Error as err:
        logger.error(f"Error: {err}")


def get_db() -> MySQLConnection:
    """Returns a connector to the MySQL database"""
    # Get database credentials from environment variables
    db_host: str = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_user: str = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password: str = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_name: str = os.getenv('PERSONAL_DATA_DB_NAME', '')

    # Connect to the database
    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )


if __name__ == '__main__':
    main()
