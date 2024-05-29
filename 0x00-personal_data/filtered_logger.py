#!/usr/bin/env python3
"""returns the log message obfuscated:"""
import re
import logging


def filter_datum(fields: list, redaction: str, message: str, separator: str) -> str:
    """returns the log message obfuscated:"""
    for field in fields:
        message = re.sub(rf'{field}=.+?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = self.filter_fields(record.msg)
        return super().format(record)

    def filter_fields(self, message: str) -> str:
        return filter_datum(self.fields, self.REDACTION, message, self.SEPARATOR)
