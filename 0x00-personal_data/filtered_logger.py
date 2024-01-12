#!/usr/bin/env python3
"""
filtered_logger module
"""

import logging
import mysql.connector
import os
import re
from typing import List


pattern = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}

PII_FIELDS = ["name", "email", "phone", "ssn", "password"]


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str,
        ) -> str:
    """Replaces specified fields in a log message with redaction."""
    extract, replace = (pattern["extract"], pattern["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)


def get_logger() -> logging.Logger:
    """Returns a configured logging.Logger object."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)

    formatter = RedactingFormatter(fields=PII_FIELDS)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a MySQL database connection."""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME", "")

    connection = mysql.connector.connect(
        host=host,
        port=3306,
        user=username,
        password=password,
        database=database
    )

    return connection


def main():
    """Retrieves all rows from the users table and displays each row under
    a filtered format."""
    fields_str = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields_str.split(',')
    query = "SELECT {} FROM users;".format(fields_str)
    info_logger = get_logger()
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(columns, row),
            )
            log_message = '{};'.format('; '.join(list(record)))
            log_record = logging.LogRecord(
                "user_data", logging.INFO, None, None, log_message, None, None
            )
            info_logger.handle(log_record)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        return filter_datum(
                self.fields, self.REDACTION, super(
                    ).format(record), self.SEPARATOR)
